from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import HospitalStaff, Doctor

class HospitalStaffForm(forms.ModelForm):
    class Meta:
        model = HospitalStaff
        fields = '__all__'

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class SignInForm(AuthenticationForm):
    pass
