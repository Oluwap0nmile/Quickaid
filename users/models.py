# users/models.py

from django.db import models
from django.contrib.auth.models import User

class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    relationship = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    from django.db import models
    

    def __str__(self):
        return f"{self.contact_name} ({self.relationship})"