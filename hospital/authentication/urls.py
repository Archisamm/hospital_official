from django.urls import path
from . import views
from .views import UserLogin, add_patient

app_name = "authentication"

urlpatterns = [
    # Registration & OTP verification
    path("signup/", views.register_view, name="signup"), 
    path("register/", views.register_view, name="register"),
    path("verify-otp/", views.verify_otp_view, name="verify_otp"),

    # Login
    path("signin/", UserLogin.as_view(), name="signin"),

    # Patient
    path("add-patient/", add_patient, name="add_patient"),
]
