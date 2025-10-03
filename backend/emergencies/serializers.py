from rest_framework import serializers
from .models import VerificationRequest, EmergencyReport
from accounts.models import UserProfile

class VerificationRequestCreateSerializer(serializers.Serializer):
    emergency_report_id = serializers.UUIDField()
    radius_km = serializers.FloatField(default=1.0)

    def validate_emergency_report_id(self, value):
        try:
            report = EmergencyReport.objects.get(report_id=value)
        except EmergencyReport.DoesNotExist:
            raise serializers.ValidationError("Emergency report not found.")
        return value

    def create(self, validated_data):
        # This will be handled in the view for geolocation logic
        pass

class UserProfileNearbySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'latitude', 'longitude']

class VerificationResponseSerializer(serializers.Serializer):
    verification_request_id = serializers.IntegerField()
    response = serializers.ChoiceField(choices=['Yes', 'No'])

    def validate(self, data):
        try:
            vreq = VerificationRequest.objects.get(id=data['verification_request_id'])
        except VerificationRequest.DoesNotExist:
            raise serializers.ValidationError({'verification_request_id': 'Verification request not found.'})
        user = self.context['request'].user.profile
        if not vreq.targeted_users.filter(id=user.id).exists():
            raise serializers.ValidationError({'user': 'User was not targeted for this verification request.'})
        return data
