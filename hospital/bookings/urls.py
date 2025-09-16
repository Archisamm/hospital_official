from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('success/', views.appointment_success, name='appointment_success'),
    path('manage/<int:appointment_id>/', views.manage_appointment, name='manage_appointment'),
    path('all/', views.ViewAppointment.as_view(), name='view_appointments'),
    path('pending/', views.PendingAppointments.as_view(), name='pending_appointments'),
    path('my/', views.my_appointments, name='my_appointments'),
]
