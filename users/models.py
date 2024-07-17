# users/models.py

from django.db import models
from django.contrib.auth.models import User

class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    relationship = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.contact_name} ({self.relationship})"