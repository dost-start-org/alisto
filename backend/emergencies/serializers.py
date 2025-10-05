from rest_framework import serializers
from .models import EmergencyType, EmergencyReport, EmergencyVerification, UserEvaluation

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

class EmergencyVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyVerification
        fields = [
            'id', 'report', 'user', 'vote', 'details',
            'image_url', 'date_created'
        ]
        read_only_fields = ['id', 'user', 'date_created']

class UserEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvaluation
        fields = [
            'id', 'report', 'user', 'stars', 'did_app_guide_clearly',
            'completion_speed', 'confidence_level', 'improvement_suggestion',
            'date_created'
        ]
        read_only_fields = ['id', 'user', 'date_created']
