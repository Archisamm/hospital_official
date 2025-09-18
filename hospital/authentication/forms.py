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


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        # Replace spaces with underscores automatically
        return username.replace(" ", "_")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={"placeholder": "Enter OTP"}))
