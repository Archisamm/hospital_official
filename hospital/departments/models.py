from django.db import models
from django.contrib.auth.models import User

DEPARTMENT_TYPE = [
    ("clinical", "Clinical"),
    ("administrative", "Administrative"),
]

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=DEPARTMENT_TYPE)

    def __str__(self):
        return f"{self.name} ({self.type})"


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=100, help_text="e.g. Receptionist, Doctor, Nurse")

    def __str__(self):
        return f"{self.user.username} - {self.role} ({self.department})"
