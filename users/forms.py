# forms.py


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pages.models import EmergencyContact 
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')





# users/forms.py




class RegistrationForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['contact_name', 'contact_email', 'contact_phone', 'relationship']
