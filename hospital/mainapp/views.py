from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Doctor, HospitalStaff
from .forms import HospitalStaffForm, DoctorForm, SignUpForm, SignInForm

# -----------------------------
# Home View
# -----------------------------
def home_view(request):
    return render(request, "home.html")

# -----------------------------
# Doctor Views
# -----------------------------
class AddDoctor(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "add_doctor.html"
    success_url = "/view_doctors/"

class ViewDoctors(ListView):
    model = Doctor
    template_name = "view_doctors.html"
    context_object_name = "doctors"

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = "doctor_details.html"
    context_object_name = "doctor"

@login_required
def book_appointment(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == "POST":
        # Here you can handle appointment booking logic
        messages.success(request, f"Appointment booked with Dr. {doctor.first_name} {doctor.last_name}")
        return redirect("view_doctors")
    return render(request, "book_appointment.html", {"doctor": doctor})


# -----------------------------
# Signup View
# -----------------------------
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("homepage")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

# -----------------------------
# Signin View
# -----------------------------
def signin_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("homepage")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "signin.html", {"form": form})


# Hospital Staff Views
# -----------------------------
def add_staff(request):
    from .forms import HospitalStaffForm
    if request.method == "POST":
        form = HospitalStaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("staff_list")
    else:
        form = HospitalStaffForm()
    return render(request, "add_staff.html", {"form": form})

def staff_list(request):
    from .models import HospitalStaff
    staff = HospitalStaff.objects.all()
    return render(request, "staff_list.html", {"staff": staff})