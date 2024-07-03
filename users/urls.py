# users/urls.py

from django.urls import path
from .views import emergency_contact_view

urlpatterns = [
    path('emergency_contact/', emergency_contact_view, name='emergency_contact'),
]
