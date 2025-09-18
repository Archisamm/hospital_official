# bookings/admin.py
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'app_date', 'status', 'handled_by')
    list_filter = ('status', 'doctor', 'handled_by')
    search_fields = ('patient__name', 'doctor__name', 'handled_by__user__username')
