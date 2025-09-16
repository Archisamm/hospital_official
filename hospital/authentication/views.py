from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView

from .forms import PatientForm, CustomRegisterForm, CustomLoginForm


# User registration
class UserRegister(CreateView):
    form_class = CustomRegisterForm
    template_name = 'signup.html'
    success_url = reverse_lazy('authentication:signin')


# User login
class UserLogin(LoginView):
    template_name = 'signin.html'
    form_class = CustomLoginForm


# Add patient view
@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user  # ✅ always link patient to logged in user
            try:
                patient.full_clean()
                patient.save()
                messages.success(request, "Patient added successfully.")
                return redirect('mainapp:view_doctors')  # ✅ send user to doctors list
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
    else:
        form = PatientForm()
    return render(request, 'add_patient_form.html', {'form': form})
