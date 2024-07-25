# users/models.py

from django.db import models
from django.contrib.auth.models import User

DEFAULT_LATITUDE = 7.759904693656651 # Example latitude for San Francisco
DEFAULT_LONGITUDE = 4.601843448762301 

class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    relationship = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField(default=DEFAULT_LATITUDE)
    longitude = models.FloatField(default=DEFAULT_LONGITUDE)
    from django.db import models
    

    def __str__(self):
        return f"{self.contact_name} ({self.relationship})"