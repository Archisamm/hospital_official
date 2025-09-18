from django.contrib import admin
from .models import Department, StaffProfile

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role', 'department')
    list_filter = ('role', 'department')
    search_fields = ('first_name', 'last_name', 'email')
