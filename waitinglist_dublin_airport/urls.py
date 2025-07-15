"""
URL configuration for waitinglist_dublin_airport project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from waitlist import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Página principal da lista de espera
    path('', views.passenger_list, name='list'),

    # Adicionar novo passageiro
    path('add/', views.add_passenger, name='add_passenger'),

    # Chamar próximo passageiro
    path('call/', views.call_next_passenger, name='call_next_passenger'),

    # Visualizar logs
    path('logs/', views.passenger_logs, name='passenger_logs'),

    # Exportações
    path('logs/pdf/', views.export_logs_pdf, name='export_logs_pdf'),
    path('logs/excel/', views.export_logs_excel, name='export_logs_excel'),

    # Detalhes e ações por passageiro
    path('passenger/<int:id>/', views.passenger_detail, name='passenger_detail'),
    path('passenger/<int:id>/skip/', views.skip_passenger, name='skip_passenger'),
    path('passenger/<int:id>/call/', views.call_specific_passenger, name='call_specific_passenger'),
    path('delete/<int:pk>/', views.delete_passenger, name='delete_passenger'),

    # Webhook do Twilio para receber resposta de SMS
    path('sms/reply/', views.twilio_reply, name='sms_reply'),
   
    path('auto-remove/<int:id>/', views.auto_remove_passenger, name='auto_remove'),

    # Cancelar vaga
    path('cancel/<int:guest_id>/', views.cancel_spot, name='cancel_spot'),
    path('cancel/confirmation/', views.cancel_confirmation, name='cancel_confirmation'),


]

