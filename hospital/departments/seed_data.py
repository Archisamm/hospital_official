from .models import Department

def seed_departments():
    clinical_departments = [
        "Outpatient Department (OPD)",
        "Inpatient Department (IPD)",
        "Intensive Care Unit (ICU)",
        "Emergency Department",
    ]

    administrative_departments = [
        "Human Resources (HR)",
        "Finance and Billing",
        "Medical Records (HIM)",
        "Administration",
        "Information Technology (IT)",
        "Supply Chain and Procurement",
    ]

    for dept in clinical_departments:
        Department.objects.get_or_create(name=dept, type="clinical")

    for dept in administrative_departments:
        Department.objects.get_or_create(name=dept, type="administrative")

    print("Departments seeded successfully.")
