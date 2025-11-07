from django.db import models
import uuid

class Agency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    logo_url = models.TextField(blank=True, null=True)
    hotline_number = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class AgencyEmergencyType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    emergency_type = models.ForeignKey('emergencies.EmergencyType', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('agency', 'emergency_type')

    def __str__(self):
        return f"{self.agency.name} - {self.emergency_type.name}"
