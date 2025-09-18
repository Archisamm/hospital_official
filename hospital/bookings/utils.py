from django.core.mail import send_mail
from django.conf import settings

def send_appointment_notification(appointment):
    """
    Send email notification to patient about scheduled appointment.
    """
    subject = f"Appointment Scheduled with Dr. {appointment.doctor.first_name}"
    message = (
        f"Hello {appointment.patient.name},\n\n"
        f"Your appointment has been scheduled with Dr. {appointment.doctor.first_name} "
        f"{appointment.doctor.last_name} on {appointment.app_date.strftime('%Y-%m-%d %H:%M')}.\n\n"
        f"Thank you!"
    )
    recipient = [appointment.patient.user.email]  # assuming patient has linked User
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient)
