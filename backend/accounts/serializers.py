
from rest_framework import serializers
from .models import User

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)

class EmailVerificationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class EmailVerificationConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    full_name = serializers.CharField(max_length=100, required=False)
    authority_level = serializers.ChoiceField(choices=['Responder', 'User', 'LGU Administrator'], required=False)
    contact_number = serializers.CharField(max_length=15, required=False)
    date_of_birth = serializers.DateField(required=False)
    address = serializers.CharField(max_length=100, required=False)
    emergency_contact_name = serializers.CharField(max_length=100, required=False, allow_null=True)
    emergency_contact_number = serializers.CharField(max_length=15, required=False, allow_null=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')
