from rest_framework import generics, permissions
from .models import Agency, AgencyEmergencyType
from .serializers import (
    AgencySerializer, AgencyDetailSerializer,
    AgencyEmergencyTypeSerializer
)

class AgencyList(generics.ListCreateAPIView):
    """
    list:
    Return a list of all registered agencies in the system.

    create:
    Register a new agency in the system.
    """
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AgencyDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    retrieve:
    Get detailed information about a specific agency.

    update:
    Update the information of a specific agency.

    partial_update:
    Update specific fields of an agency.

    destroy:
    Remove a specific agency from the system.
    """
    queryset = Agency.objects.all()
    serializer_class = AgencyDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AgencyEmergencyTypeList(generics.ListCreateAPIView):
    """
    list:
    Get a list of all emergency types that agencies can handle.

    create:
    Associate a new emergency type with an agency.
    """
    queryset = AgencyEmergencyType.objects.all()
    serializer_class = AgencyEmergencyTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AgencyEmergencyTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    retrieve:
    Get details about a specific agency-emergency type association.

    update:
    Update an agency-emergency type association.

    partial_update:
    Update specific fields of an agency-emergency type association.

    destroy:
    Remove an emergency type association from an agency.
    """
    queryset = AgencyEmergencyType.objects.all()
    serializer_class = AgencyEmergencyTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
