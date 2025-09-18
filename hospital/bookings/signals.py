from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from .utils import send_appointment_notification

@receiver(post_save, sender=Appointment)
def notify_patient(sender, instance, created, **kwargs):
    """
    Automatically notify patient when an appointment is scheduled.
    """
    if instance.status == "scheduled":
        send_appointment_notification(instance)
