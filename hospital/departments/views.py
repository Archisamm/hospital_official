from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Department, StaffProfile
from .forms import DepartmentForm, StaffProfileForm

# List Departments
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/department_list.html', {'departments': departments})

# Add Department
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully")
            return redirect('departments:department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/add_department.html', {'form': form})

# Add Staff
def add_staff(request):
    if request.method == 'POST':
        form = StaffProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff added successfully")
            return redirect('departments:staff_list')
    else:
        form = StaffProfileForm()
    return render(request, 'departments/add_staff.html', {'form': form})

# List Staff
def staff_list(request):
    staff_members = StaffProfile.objects.all()
    return render(request, 'departments/staff_list.html', {'staff_members': staff_members})
