from rest_framework import serializers
from .models import Agency, AgencyEmergencyType
from emergencies.serializers import EmergencyTypeSerializer

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['id', 'name', 'logo_url', 'hotline_number', 'latitude', 'longitude']

class AgencyEmergencyTypeSerializer(serializers.ModelSerializer):
    agency = AgencySerializer(read_only=True)
    emergency_type = EmergencyTypeSerializer(read_only=True)

    class Meta:
        model = AgencyEmergencyType
        fields = ['id', 'agency', 'emergency_type']

class AgencyDetailSerializer(serializers.ModelSerializer):
    emergency_types = EmergencyTypeSerializer(many=True, read_only=True, source='agencyemergencytype_set.emergency_type')

    class Meta:
        model = Agency
        fields = ['id', 'name', 'logo_url', 'hotline_number', 'latitude', 'longitude', 'emergency_types']