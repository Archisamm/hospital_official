import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import View
from .models import Appointment
from authentication.models import Patient
from departments.models import StaffProfile
from mainapp.models import Doctor

# ---------------- Appointment Booking with Razorpay ----------------
@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    user_patients = Patient.objects.filter(user=request.user)

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        app_date = request.POST.get('app_date')
        patient = get_object_or_404(Patient, id=patient_id, user=request.user)

        # 1️⃣ Create appointment
        appointment = Appointment.objects.create(
            user=request.user,
            doctor=doctor,
            patient=patient,
            app_date=app_date
        )

        # 2️⃣ Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # 3️⃣ Create Razorpay order
        amount_in_paise = int(appointment.fee * 100)  # Convert rupees to paise
        order_currency = 'INR'
        order_receipt = f'order_{appointment.id}'

        razorpay_order = client.order.create(dict(
            amount=amount_in_paise,
            currency=order_currency,
            receipt=order_receipt,
            payment_capture='1'
        ))

        # 4️⃣ Save order id to appointment
        appointment.razorpay_order_id = razorpay_order['id']
        appointment.save()

        # 5️⃣ Render Razorpay checkout page
        return render(request, 'bookings/razorpay_checkout.html', {
            'appointment': appointment,
            'razorpay_order': razorpay_order,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount_in_paise': amount_in_paise,
        })

    return render(request, 'bookings/book_appointment.html', {
        'doctor': doctor,
        'patients': user_patients
    })


# ---------------- Appointment Success Page ----------------
@login_required
def appointment_success(request):
    return render(request, 'bookings/appointment_success.html')


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
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.handled_by = staff
            appointment.save()
            return HttpResponse(f"Status updated to {new_status}")
        else:
            return HttpResponse("Invalid status.")

    return render(request, 'bookings/manage_appointment.html', {'appointment': appointment})


# ---------------- View All Appointments ----------------
class ViewAppointment(View):
    def get(self, request):
        appointments = Appointment.objects.all()
        return render(request, 'bookings/view_appointments.html', {'appointments': appointments})


# ---------------- View Pending Appointments ----------------
class PendingAppointments(View):
    def get(self, request):
        pending = Appointment.objects.filter(status='pending')
        return render(request, 'bookings/pending_appointments.html', {'appointments': pending})


# ---------------- View My Appointments ----------------
@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'bookings/my_appointments.html', {'appointments': appointments})
