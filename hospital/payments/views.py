# payments/views.py
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt  # 👈 import this
from bookings.models import Appointment
from .models import Payment, PaymentAttempt
import razorpay

# Razorpay client setup
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def create_order(request, booking_id):
    """Create a Razorpay order for a booking"""
    appointment = get_object_or_404(Appointment, id=booking_id)

    amount = int(appointment.fee * 100)  # amount in paise
    currency = "INR"

    razorpay_order = razorpay_client.order.create(
        dict(amount=amount, currency=currency, payment_capture="1")
    )

    # Ensure payment record exists
    payment, created = Payment.objects.get_or_create(
        appointment=appointment,
        user=request.user,
        defaults={"amount": appointment.fee, "status": "created"},
    )

    # Save PaymentAttempt for this Razorpay order
    PaymentAttempt.objects.create(
        payment=payment,
        razorpay_order_id=razorpay_order["id"],
    )

    context = {
        "appointment": appointment,
        "payment": payment,
        "razorpay_order": razorpay_order,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    }
    return render(request, "checkout.html", context)


@csrf_exempt
def payment_success(request):
    """Handle successful payment"""
    if request.method == "POST":
        try:
            razorpay_payment_id = request.POST.get("razorpay_payment_id")
            razorpay_order_id = request.POST.get("razorpay_order_id")
            razorpay_signature = request.POST.get("razorpay_signature")

            if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
                return HttpResponseBadRequest("Missing payment parameters.")

            # Verify signature
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }
            razorpay_client.utility.verify_payment_signature(params_dict)

            # Find the attempt
            attempt = PaymentAttempt.objects.filter(
                razorpay_order_id=razorpay_order_id
            ).first()
            if not attempt:
                return HttpResponseBadRequest("Payment attempt not found.")

            # Update attempt
            attempt.razorpay_payment_id = razorpay_payment_id
            attempt.razorpay_signature = razorpay_signature
            attempt.save()

            # Update Payment
            payment = attempt.payment
            payment.status = "paid"
            payment.save()

            # Update Appointment (⚠️ make sure 'confirmed' is valid in your model)
            if payment.appointment:
                payment.appointment.status = "confirmed"
                payment.appointment.save()

            return render(request, "success.html", {"payment": payment})

        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest("Payment verification failed: Signature mismatch")
        except Exception as e:
            return HttpResponseBadRequest(f"Payment verification failed: {str(e)}")
    return HttpResponseBadRequest("Invalid request")


@csrf_exempt
def payment_failure(request):
    """Handle failed payment"""
    if request.method == "POST":
        razorpay_order_id = request.POST.get("razorpay_order_id")

        # Find the PaymentAttempt
        attempt = PaymentAttempt.objects.filter(
            razorpay_order_id=razorpay_order_id
        ).first()
        if attempt:
            # Update attempt status
            attempt.razorpay_payment_id = request.POST.get("razorpay_payment_id")
            attempt.save()

            # Mark Payment as failed
            payment = attempt.payment
            payment.status = "failed"
            payment.save()

            # Keep appointment as "pending" until retried
            if payment.appointment and payment.appointment.status == "pending":
                payment.appointment.status = "cancelled"
                payment.appointment.save()

        return render(request, "failure.html", {"payment": attempt.payment if attempt else None})
    return HttpResponseBadRequest("Invalid request")
