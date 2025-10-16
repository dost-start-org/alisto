from rest_framework import serializers
from .models import EmergencyContact, ContactRedirection
from emergencies.serializers import EmergencyTypeSerializer

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ['id', 'name', 'contact_number', 'description', 'type']

class ContactRedirectionSerializer(serializers.ModelSerializer):
    contact = EmergencyContactSerializer(read_only=True)
    emergency_type = EmergencyTypeSerializer(read_only=True)

    class Meta:
        model = ContactRedirection
        fields = ['id', 'contact', 'emergency_type']

class EmergencyContactDetailSerializer(serializers.ModelSerializer):
    emergency_types = EmergencyTypeSerializer(many=True, read_only=True, source='contactredirection_set.emergency_type')

    class Meta:
        model = EmergencyContact
        fields = ['id', 'name', 'contact_number', 'description', 'type', 'emergency_types']