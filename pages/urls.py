# pages/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.services, name='services'),
    path('services/', views.emergency_contact_view, name='services'),
]
