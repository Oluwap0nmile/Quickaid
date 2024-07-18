from django.urls import path
from .views import login_view, register, emergency_contact_view, EmergencyContactDeleteView, send_emergency_sms, save_location, register_chat_id

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('emergency_contact/', emergency_contact_view, name='emergency_contact'),
    path('delete/<int:pk>/', EmergencyContactDeleteView.as_view(), name='emergency_contact_delete'),
    path('send_emergency_sms/', send_emergency_sms, name='send_emergency_sms'),
    path('save_location/', save_location, name='save_location'),
    path('register_chat_id/', register_chat_id, name='register_chat_id'),
]
