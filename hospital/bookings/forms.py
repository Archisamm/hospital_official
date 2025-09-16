from django import forms
from .models import Appointment
from mainapp.models import Doctor
from authentication.models import Patient  # Assuming Patient is in authentication.models

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'app_date']  # doctor is set in the view
        widgets = {
            'app_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['patient'].queryset = Patient.objects.filter(user=user)
