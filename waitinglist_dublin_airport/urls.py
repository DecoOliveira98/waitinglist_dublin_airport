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
    path('passenger/<int:id>/call/', views.call_specific_passenger, name='call_specific_passenger'),
    path('delete/<int:pk>/', views.delete_passenger, name='delete_passenger'),

    # Cancelar vaga
    path('cancel/<int:guest_id>/', views.cancel_spot, name='cancel_spot'),
    path('cancel/confirmation/', views.cancel_confirmation, name='cancel_confirmation'),

    # Auto-remover passageiro
    path('auto-remove/<int:id>/', views.auto_remove_passenger, name='auto_remove'),

    # Limpar logs por dia
    path('logs/clear-by-day/', views.clear_logs_by_day, name='clear_logs_by_day'),
    path('logs/clear-all/', views.clear_all_logs, name='clear_all_logs'),

    # Página de sucesso ao deletar logs
    path('logs/deleted/', views.logs_deleted_success, name='logs_deleted_success'),



]
