

from django import forms
from .models import EmergencyContact
from pages.models import EmergencyContact

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['contact_name', 'contact_email', 'contact_phone', 'relationship']
