from rest_framework import serializers
from .models import Agency, AgencyEmergencyType
from emergencies.serializers import EmergencyTypeSerializer
from core.services.file_service import FileService

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['id', 'name', 'logo_url', 'hotline_number', 'latitude', 'longitude']
    
    def validate_logo_url(self, value):
        """Validate and process logo_url field (accepts base64 or URL)"""
        if not value:
            return value
        
        # Process the image (uploads to Cloudinary if base64)
        success, result = FileService.process_image_field(value, folder='agency_logos')
        
        if not success:
            raise serializers.ValidationError(result)
        
        return result

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