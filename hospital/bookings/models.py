# bookings/models.py
from django.db import models
from authentication.models import Patient
from django.core.exceptions import ValidationError
from mainapp.models import Doctor
from django.contrib.auth.models import User


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval. Please wait...'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
        ('rescheduled', 'Rescheduled'),
        ('confirmed', 'Confirmed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    app_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=20)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)

    # Razorpay integration fields
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    advance_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)

    # Staff handling this appointment (optional)
    handled_by = models.ForeignKey(
        'departments.StaffProfile',  # string reference to avoid circular import
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Staff member responsible for this appointment"
    )

    class Meta:
        # Removed UniqueConstraint to avoid duplicate error messages
        ordering = ['app_date']

    @property
    def total_amount(self):
        """Returns consultation fee set by doctor or default advance fee"""
        if self.doctor and hasattr(self.doctor, "booking_amount"):
            return int(self.doctor.booking_amount)
        return int(self.advance_fee)

    def clean(self):
        """Prevent double booking of same doctor at same time."""
        if Appointment.objects.filter(doctor=self.doctor, app_date=self.app_date).exclude(id=self.id).exists():
            raise ValidationError("This doctor already has an appointment at this time.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Runs validation (including clean())
        super().save(*args, **kwargs)

    def __str__(self):
        patient_name = getattr(self.patient, 'name', 'Unknown')
        doctor_name = getattr(self.doctor, 'name', 'Unknown')
        date_str = self.app_date.strftime('%Y-%m-%d %H:%M') if self.app_date else 'Unknown'
        return f"{patient_name} with Dr. {doctor_name} on {date_str}"
