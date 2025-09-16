from django import forms
from .models import Patient
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget
from datetime import date

# -------------------------------
# Custom User Registration Form
# -------------------------------
class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# -------------------------------
# Custom Login Form
# -------------------------------
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# -------------------------------
# Patient Form
# -------------------------------
class PatientForm(forms.ModelForm):
    # Dynamic DOB dropdown: 1900 → current year
    current_year = date.today().year
    dob = forms.DateField(
        widget=SelectDateWidget(years=range(1900, current_year + 1))
    )

    class Meta:
        model = Patient
        # Exclude user; will be set from request in the view
        exclude = ['user']
