from django import forms
from .models import Department, StaffProfile

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['first_name', 'last_name', 'email', 'role', 'department']
