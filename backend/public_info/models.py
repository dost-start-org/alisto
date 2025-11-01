from django.db import models
from django.conf import settings
import uuid

class EmergencyContact(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('Hotline', 'Hotline'),
        ('General Contact', 'General Contact')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.contact_number}"

class UserEmergencyContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    relationship = models.CharField(max_length=100, null=True, blank=True)
    photo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.user}'s {self.relationship}"

class ContactRedirection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE)
    emergency_type = models.ForeignKey('emergencies.EmergencyType', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.emergency_type.name} -> {self.contact.name}"