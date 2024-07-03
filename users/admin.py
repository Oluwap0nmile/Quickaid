from django.contrib import admin

# Register your models here.
from .models import EmergencyContact
@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'contact_phone', 'relationship', 'user')
    search_fields = ('contact_name', 'contact_phone', 'relationship', 'user__username')