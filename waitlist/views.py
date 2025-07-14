import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from django.utils.html import escape
from twilio.rest import Client
from xhtml2pdf import pisa
import openpyxl
from openpyxl.utils import get_column_letter
from .models import Passenger, PassengerLog
from django.core.mail import send_mail  
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import escape
import re
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import os

# Página inicial: lista de passageiros na fila
def passenger_list(request):
    passengers = Passenger.objects.order_by('joined_at')
    return render(request, 'waitlist/list.html', {'passengers': passengers})

# Chamar passageiro específico

def call_specific_passenger(request, id):
    passenger = get_object_or_404(Passenger, id=id)

    # Registrar no log
    PassengerLog.objects.create(
        name=passenger.name,
        country_code=passenger.country_code,
        phone=passenger.local_phone,
        guests=passenger.guests,
        time_joined=passenger.joined_at
    )

    # Mensagem de notificação
    message = f"Hi {passenger.name}, your lounge spot is ready. Please proceed to reception."

    if passenger.notification_method == 'sms':
        send_sms(to=passenger.full_phone, message=message)

    elif passenger.notification_method == 'email' and passenger.email:
        subject = "Lounge Spot Ready"
        from_email = "noreply@liffeylounge.com"
        to_email = passenger.email

        # Renderiza HTML e envia como e-mail alternativo
        try:
            html_content = render_to_string('email/passenger_called.html', {'name': passenger.name})
            msg = EmailMultiAlternatives(subject, '', from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            # Fallback para e-mail simples se der erro no template
            send_mail(subject, message, from_email, [to_email])

    # Remove o passageiro da fila
    passenger.delete()
    
    return redirect('list')



# Adicionar passageiro


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

        message = f"Hi {name}, you've been added to the lounge waiting list. You will be notified when your spot is ready."

        if notification_method == 'sms':
            send_sms(to=passenger.full_phone, message=message)

        elif notification_method == 'email' and passenger.email:
            subject = "Lounge Waiting List Confirmation"
            from_email = "noreply@LiffeyLounge.com"  # coloque um e-mail válido do seu domínio
            to_email = passenger.email

            context = {
                'name': passenger.name,
                'guests': passenger.guests,
            }

            html_content = render_to_string('email/added_to_queue.html', context)
            msg = EmailMultiAlternatives(subject, '', from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        return redirect('list')

    return render(request, 'waitlist/add.html')


# Chamar próximo passageiro
def call_next_passenger(request):
    if request.method == 'POST':
        next_passenger = Passenger.objects.order_by('joined_at').first()
        if next_passenger:
            # Registrar no log
            PassengerLog.objects.create(
                name=next_passenger.name,
                country_code=next_passenger.country_code,
                phone=next_passenger.local_phone,
                guests=next_passenger.guests,
                time_joined=next_passenger.joined_at
            )

            message = (
                f"Hi {next_passenger.name}, your lounge spot is ready. "
                "Please proceed to reception. You have 10 minutes to arrive. "
                "If not, reply '1' to cancel."
            )

            if next_passenger.notification_method == 'sms':
                send_sms(to=next_passenger.full_phone, message=message)

            elif next_passenger.notification_method == 'email' and next_passenger.email:
                subject = "🚨 Your Lounge Spot is Ready!"
                from_email = "noreply@LiffeyLounge.com"
                to_email = next_passenger.email

                context = {
                    'name': next_passenger.name,
                    'guests': next_passenger.guests,
                }

                html_content = render_to_string('email/passenger_called.html', context)
                msg = EmailMultiAlternatives(subject, '', from_email, [to_email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            next_passenger.delete()

    return redirect('list')

# Detalhes do passageiro
def passenger_detail(request, id):
    passenger = get_object_or_404(Passenger, id=id)
    return render(request, 'waitlist/passenger_detail.html', {'passenger': passenger})


# Pular passageiro (joga para o final da fila)
def skip_passenger(request, id):
    passenger = get_object_or_404(Passenger, id=id)
    passenger.joined_at = timezone.now()
    passenger.save()
    return redirect('passenger_list')


# Remover passageiro
def delete_passenger(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    passenger.delete()
    return redirect('passenger_list')


# Exportar logs em PDF
def export_logs_pdf(request):
    logs = PassengerLog.objects.order_by('-time_called')
    template_path = 'waitlist/logs_pdf.html'
    context = {'logs': logs}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="passenger_logs.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response


# Exportar logs em Excel
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

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=passenger_logs.xlsx'
    wb.save(response)
    return response


# Exibir logs
def passenger_logs(request):
    logs = PassengerLog.objects.order_by('-time_called')
    return render(request, 'waitlist/logs.html', {'logs': logs})


# Enviar SMS usando Twilio
def send_sms(to, message):
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_=os.environ.get("TWILIO_PHONE_NUMBER"),
        to=to
    )
