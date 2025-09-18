import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import View
from django.core.exceptions import ValidationError

from .models import Appointment
from authentication.models import Patient
from authentication.forms import PatientForm
from departments.models import StaffProfile
from mainapp.models import Doctor
from .utils import send_appointment_notification  # notification function


# ---------------- Appointment Booking (Patient) ----------------
@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    user_patients = Patient.objects.filter(user=request.user)
    error_message = None

    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        app_date = request.POST.get("app_date")

        # Use existing patient or create a new one
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id, user=request.user)
        else:
            form = PatientForm(request.POST)
            if form.is_valid():
                patient = form.save(commit=False)
                patient.user = request.user
                patient.full_clean()
                patient.save()
            else:
                return render(request, "bookings/book_appointment.html", {
                    "doctor": doctor,
                    "patients": user_patients,
                    "form": form
                })

        try:
            # Create and validate appointment
            appointment = Appointment(
                user=request.user,
                doctor=doctor,
                patient=patient,
                app_date=app_date
            )
            appointment.full_clean()  # ensures doctor availability
            appointment.save()

            # Razorpay payment order
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            amount_in_paise = int(appointment.fee * 100)
            order_receipt = f"order_{appointment.id}"
            razorpay_order = client.order.create(dict(
                amount=amount_in_paise,
                currency="INR",
                receipt=order_receipt,
                payment_capture="1"
            ))

            appointment.razorpay_order_id = razorpay_order["id"]
            appointment.save()

            return render(request, "bookings/razorpay_checkout.html", {
                "appointment": appointment,
                "razorpay_order": razorpay_order,
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                "amount_in_paise": amount_in_paise,
            })

        except ValidationError as e:
            error_message = e.message_dict.get("__all__", [""])[0]

    form = PatientForm()
    return render(request, "bookings/book_appointment.html", {
        "doctor": doctor,
        "patients": user_patients,
        "form": form,
        "error_message": error_message
    })


# ---------------- Appointment Success Page ----------------
@login_required
def appointment_success(request):
    return render(request, "bookings/appointment_success.html")


# ---------------- Manage Appointment (Receptionist) ----------------
@login_required
def manage_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    staff = StaffProfile.objects.filter(
        user=request.user,
        department__name="Outpatient Department (OPD)",
        role="Receptionist"
    ).first()

    if not staff:
        return HttpResponse("You are not authorized to manage this appointment.")

    if request.method == "POST":
        new_status = request.POST.get("status")
        new_date = request.POST.get("app_date")  # receptionist can update date/time
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            if new_date:
                appointment.app_date = new_date
            appointment.handled_by = staff
            appointment.save()

            # Notify patient about new schedule
            send_appointment_notification(appointment)

            return HttpResponse("Appointment updated and patient notified.")
        else:
            return HttpResponse("Invalid status.")

    return render(request, "bookings/manage_appointment.html", {"appointment": appointment})


# ---------------- View All Appointments ----------------
class ViewAppointment(View):
    def get(self, request):
        appointments = Appointment.objects.all()
        return render(request, "bookings/view_appointments.html", {"appointments": appointments})


# ---------------- View Pending Appointments ----------------
class PendingAppointments(View):
    def get(self, request):
        pending = Appointment.objects.filter(status="pending")
        return render(request, "bookings/pending_appointments.html", {"appointments": pending})


# ---------------- View My Appointments ----------------
@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, "bookings/my_appointments.html", {"appointments": appointments})
