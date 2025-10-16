from rest_framework import serializers
from .models import Responder
from accounts.serializers import UserSerializer
from agencies.serializers import AgencySerializer

class ResponderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    agency = AgencySerializer(read_only=True)

    class Meta:
        model = Responder
        fields = ['id', 'user', 'agency']

class ResponderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responder
        fields = ['user', 'agency']