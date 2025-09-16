from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'mainapp'

urlpatterns = [
    # Home
    path('', views.home_view, name='homepage'),

    # Auth (optional, since auth is under authentication app too)
    path('logout/', auth_views.LogoutView.as_view(next_page='mainapp:homepage'), name='logout'),

    # Doctors
    path('add_doctor/', views.AddDoctor.as_view(), name='add_doctor'),
    path('view_doctors/', views.ViewDoctors.as_view(), name='view_doctors'),
    path('doctor/<int:pk>/', views.DoctorDetailView.as_view(), name='doc_details'),
    path('doctor/book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),

    # Staff
    path('add_staff/', views.add_staff, name='add_staff'),
    path('staff_list/', views.staff_list, name='staff_list'),
]
