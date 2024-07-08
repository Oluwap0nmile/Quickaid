# users/urls.py

from django.urls import path
from .views import emergency_contact_view,EmergencyContactDeleteView
from users.views import send_emergency_message

urlpatterns = [
    path('emergency_contact/', emergency_contact_view, name='emergency_contact'),
    path('emergency_contact/delete/<int:pk>/', EmergencyContactDeleteView.as_view(), name='emergency_contact_delete'),
    path('send_emergency_message/', send_emergency_message, name='send_emergency_message'),


]

