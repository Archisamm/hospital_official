from django.db import models

# -------------------------------
# Hospital Staff Model
# -------------------------------
class HospitalStaff(models.Model):
    STAFF_ROLES = [
        ('admin', 'Administrator'),
        ('nurse', 'Nurse'),
        ('receptionist', 'Receptionist'),
        ('lab', 'Lab Technician'),
        ('janitor', 'Janitor'),
        ('other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    role = models.CharField(max_length=50, choices=STAFF_ROLES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"


# -------------------------------
# Doctor Model
# -------------------------------
class Doctor(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    DEPARTMENT_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('general', 'General'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    specialization = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)  # Added for profile/carousel
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.department}"
