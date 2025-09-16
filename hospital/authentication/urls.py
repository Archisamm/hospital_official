from django.urls import path
from . import views
from .views import UserRegister, UserLogin

app_name = 'authentication'

urlpatterns = [
    # User registration & login
    path('register/', UserRegister.as_view(), name='signup'),
    path('signin/', UserLogin.as_view(), name='signin'),

    # Patients
    path('patients/', views.add_patient, name='add_patient'),
]
