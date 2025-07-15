import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMultiAlternatives
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from xhtml2pdf import pisa
import openpyxl
from openpyxl.utils import get_column_letter
from decouple import config

from .models import Passenger, PassengerLog

# ---------------- Email + SMS Templates ----------------
message_addToQueue = (
    "Hi {passenger.name}, you've been added to the lounge waiting list. "
    "You will be notified when your spot is ready."
)
message_called = (
    "Hi {passenger.name}, your lounge spot is ready. "
    "Please proceed to reception. You have 10 minutes to arrive. "
    "If not, reply '1' to cancel."
)

# ---------------- Utilidade ----------------

def send_sms(to, message):
    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    from_number = config('TWILIO_PHONE_NUMBER')
    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_=from_number, to=to)

# ---------------- Views ----------------

def cancel_confirmation(request):
    return render(request, 'cancel_confirmation.html')

def cancel_spot(request, guest_id):
    guest = get_object_or_404(Passenger, id=guest_id)
    guest.delete()
    return HttpResponse("✅ Your spot has been successfully cancelled.")

@csrf_exempt
def twilio_reply(request):
    if request.method == 'POST':
        from_number = request.POST.get('From', '').strip()
        body = request.POST.get('Body', '').strip()
        response = MessagingResponse()

        if body == "1":
            passenger = next((p for p in Passenger.objects.all() if p.full_phone == from_number), None)
            if passenger:
                passenger.delete()
                response.message("✅ You have been removed from the waiting list.")
            else:
                response.message("❌ We couldn't find your booking.")
        else:
            response.message("Send '1' if you wish to cancel your waiting list position.")

        return HttpResponse(str(response), content_type="application/xml")
    return HttpResponse("Invalid method", status=405)

def add_passenger(request):
    if request.method == 'POST':
        name = escape(request.POST['name'])
        country_code = request.POST['country_code']
        local_phone = re.sub(r'\D', '', request.POST['local_phone'])
        guests = int(request.POST.get('guests', 0))
        notification_method = request.POST.get('notification_method', 'sms')
        email = request.POST.get('email', '').strip() or None

        passenger = Passenger.objects.create(
            name=name,
            country_code=country_code,
            local_phone=local_phone,
            guests=guests,
            notification_method=notification_method,
            email=email
        )

        message = message_addToQueue.format(passenger=passenger)

        if notification_method == 'sms':
            send_sms(to=passenger.full_phone, message=message)

        elif notification_method == 'email' and passenger.email:
            cancel_url = request.build_absolute_uri(f"/cancel/{passenger.id}/")
            subject = "The Liffey Lounge Waiting List Confirmation"
            from_email = config('HOST_USER')
            to_email = passenger.email
            context = {'name': passenger.name, 'guests': passenger.guests, 'cancel_url': cancel_url}
            html_content = render_to_string('email/added_to_queue.html', context)
            msg = EmailMultiAlternatives(subject, '', from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        return redirect('list')

    return render(request, 'waitlist/add.html')

def call_specific_passenger(request, id):
    passenger = get_object_or_404(Passenger, id=id)
    passenger.called = True
    passenger.called_at = timezone.now()
    passenger.save()

    PassengerLog.objects.create(
        name=passenger.name,
        country_code=passenger.country_code,
        phone=passenger.local_phone,
        guests=passenger.guests,
        time_joined=passenger.joined_at
    )

    message = message_called.format(passenger=passenger)

    if passenger.notification_method == 'sms':
        send_sms(to=passenger.full_phone, message=message)

    elif passenger.notification_method == 'email' and passenger.email:
        subject = "Lounge Spot Ready"
        from_email = config('HOST_USER')
        to_email = passenger.email
        context = {'name': passenger.name}
        try:
            html_content = render_to_string('email/passenger_called.html', context)
            msg = EmailMultiAlternatives(subject, '', from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception:
            send_mail(subject, message, from_email, [to_email])

    return redirect('list')

def call_next_passenger(request):
    if request.method == 'POST':
        next_passenger = Passenger.objects.filter(called=False).order_by('joined_at').first()
        if next_passenger:
            return call_specific_passenger(request, next_passenger.id)
    return redirect('list')

def auto_remove_passenger(request, id):
    passenger = get_object_or_404(Passenger, id=id)
    if passenger.called and passenger.called_at:
        elapsed = timezone.now() - passenger.called_at
        if elapsed.total_seconds() >= 600:
            passenger.delete()
            return HttpResponse("⛔ Passenger Removed after expiration.")
        return HttpResponse("⏳ Not expired yet.")
    return HttpResponse("❌Passenger not called or data not valid.")

def delete_passenger(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    passenger.delete()
    return redirect('list')

def skip_passenger(request, id):
    passenger = get_object_or_404(Passenger, id=id)
    passenger.joined_at = timezone.now()
    passenger.save()
    return redirect('passenger_list')

def passenger_list(request):
    passengers = Passenger.objects.order_by('joined_at')
    return render(request, 'waitlist/list.html', {'passengers': passengers})

def passenger_detail(request, id):
    passenger = get_object_or_404(Passenger, id=id)
    return render(request, 'waitlist/passenger_detail.html', {'passenger': passenger})

def passenger_logs(request):
    logs = PassengerLog.objects.order_by('-time_called')
    return render(request, 'waitlist/logs.html', {'logs': logs})

def export_logs_pdf(request):
    logs = PassengerLog.objects.order_by('-time_called')
    template_path = 'waitlist/logs_pdf.html'
    context = {'logs': logs}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="passenger_logs.pdf"'
    html = get_template(template_path).render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response

def export_logs_excel(request):
    logs = PassengerLog.objects.order_by('-time_called')
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Passenger Logs"
    headers = ['Name', 'Phone', 'Guests', 'Time Joined', 'Time Called']
    ws.append(headers)

    for log in logs:
        ws.append([
            log.name,
            f"+{log.country_code}{log.phone}",
            log.guests,
            log.time_joined.strftime("%Y-%m-%d %H:%M"),
            log.time_called.strftime("%Y-%m-%d %H:%M") if log.time_called else ''
        ])

    for i, column in enumerate(ws.columns, 1):
        max_length = max(len(str(cell.value or "")) for cell in column)
        ws.column_dimensions[get_column_letter(i)].width = max_length + 2

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=passenger_logs.xlsx'
    wb.save(response)
    return response
