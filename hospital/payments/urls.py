# payments/urls.py
from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [    
    path("checkout/<int:booking_id>/", views.create_order, name="create_order"),
    path("success/", views.payment_success, name="payment_success"),
    path("failure/", views.payment_failure, name="payment_failure"),
    
]
