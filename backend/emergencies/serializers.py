from rest_framework import serializers
from .models import EmergencyType, EmergencyReport, EmergencyVerification, UserEvaluation
from core.services.file_service import FileService

class EmergencyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyType
        fields = ['id', 'name', 'icon_type']

class EmergencyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyReport
        fields = [
            'id', 'emergency_type', 'user', 'longitude', 'latitude',
            'details', 'verification_status', 'status', 'image_url',
            'date_created'
        ]
        read_only_fields = ['id', 'user', 'verification_status', 'date_created']
    
    def validate_longitude(self, value):
        # Philippines longitude range approximately: 116.93° to 126.34° E
        if not (116.93 <= value <= 126.34):
            raise serializers.ValidationError("Longitude must be within the Philippines (116.93° to 126.34° E)")
        return value

    def validate_latitude(self, value):
        # Philippines latitude range approximately: 4.23° to 21.12° N
        if not (4.23 <= value <= 21.12):
            raise serializers.ValidationError("Latitude must be within the Philippines (4.23° to 21.12° N)")
        return value

    def validate_details(self, value):
        if value and len(value) < 10:
            raise serializers.ValidationError("Details must be at least 10 characters long")
        return value

    def validate_image_url(self, value):
        """Validate and process image_url field (accepts base64 or URL)"""
        if not value:
            return value
        
        # Process the image (uploads to Cloudinary if base64)
        success, result = FileService.process_image_field(value, folder='emergency_reports')
        
        if not success:
            raise serializers.ValidationError(result)
        
        return result
    
    def create(self, validated_data):
        """Override create to handle image upload"""
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Override update to handle image upload"""
        return super().update(instance, validated_data)

class EmergencyVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyVerification
        fields = [
            'id', 'report', 'user', 'vote', 'details',
            'image_url', 'date_created'
        ]
        read_only_fields = ['id', 'user', 'date_created']

    def validate_details(self, value):
        if value and len(value.strip()) < 5:
            raise serializers.ValidationError("Verification details must be at least 5 characters long")
        return value.strip() if value else value

    def validate_image_url(self, value):
        """Validate and process image_url field (accepts base64 or URL)"""
        if not value:
            return value
        
        # Process the image (uploads to Cloudinary if base64)
        success, result = FileService.process_image_field(value, folder='emergency_verifications')
        
        if not success:
            raise serializers.ValidationError(result)
        
        return result
        
    def validate(self, data):
        # If voting false (denying), details should be required
        if data.get('vote') is False and not data.get('details'):
            raise serializers.ValidationError({
                "details": "Details are required when denying an emergency report"
            })
        return data

class UserEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvaluation
        fields = [
            'id', 'report', 'user', 'stars', 'did_app_guide_clearly',
            'completion_speed', 'confidence_level', 'improvement_suggestion',
            'date_created'
        ]
        read_only_fields = ['id', 'user', 'date_created']

    def validate_stars(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Stars rating must be between 1 and 5")
        return value

    def validate_improvement_suggestion(self, value):
        if value and len(value.strip()) < 10:
            raise serializers.ValidationError("Improvement suggestion must be at least 10 characters long")
        return value.strip() if value else value

    def validate(self, data):
        # If rating is low (1 or 2 stars), require improvement suggestion
        if data.get('stars') in [1, 2] and not data.get('improvement_suggestion'):
            raise serializers.ValidationError({
                "improvement_suggestion": "Please provide improvement suggestions for low ratings"
            })
        return data
