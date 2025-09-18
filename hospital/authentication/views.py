from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings

from .forms import PatientForm, CustomLoginForm, RegisterForm, OTPForm
from .models import EmailOTP


# ---------------- User Registration with OTP ----------------
def register_view(request):
    """
    Handles user registration with OTP email verification.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create inactive user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active = False
            user.save()

            # Generate or reuse OTP object
            otp_obj, _ = EmailOTP.objects.get_or_create(user=user)
            otp = otp_obj.generate_otp()

            # Send OTP email
            subject = "Your OTP Code"
            message = f"Welcome {user.username},\n\nYour OTP is {otp}. It expires in 5 minutes."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            # Store user in session until OTP verified
            request.session["pending_user"] = user.id
            messages.info(request, f"An OTP has been sent to {user.email}")
            return redirect("authentication:verify_otp")
    else:
        form = RegisterForm()

    return render(request, "authentication/register.html", {"form": form})


def verify_otp_view(request):
    """
    Verifies the OTP entered by the user and activates the account.
    """
    user_id = request.session.get("pending_user")
    if not user_id:
        messages.error(request, "Session expired. Please register again.")
        return redirect("authentication:register")

    user = User.objects.get(id=user_id)
    otp_obj = EmailOTP.objects.get(user=user)

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["otp"] == otp_obj.otp:
                # Activate and log in user
                user.is_active = True
                user.save()
                otp_obj.delete()
                login(request, user)
                messages.success(request, "Account verified successfully!")
                return redirect("mainapp:view_doctors")
            else:
                form.add_error("otp", "Invalid OTP")
    else:
        form = OTPForm()

    return render(request, "authentication/verify_otp.html", {"form": form, "email": user.email})


# ---------------- User Login ----------------
class UserLogin(LoginView):
    """
    Handles user login with custom login form.
    """
    template_name = "authentication/signin.html"
    form_class = CustomLoginForm


# ---------------- Add Patient ----------------
@login_required
def add_patient(request):
    """
    Allows logged-in users to add a patient profile.
    """
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            try:
                patient.full_clean()
                patient.save()
                messages.success(request, "Patient added successfully.")
                return redirect("mainapp:view_doctors")
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
    else:
        form = PatientForm()

    return render(request, "add_patient_form.html", {"form": form})
