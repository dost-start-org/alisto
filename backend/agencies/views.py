from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(
        operation_summary="List agencies",
        operation_description="Return a list of all registered agencies in the system.",
        tags=['Agencies'],
        responses={200: AgencySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create agency",
        operation_description="Register a new agency in the system.",
        tags=['Agencies'],
        request_body=AgencySerializer,
        responses={201: AgencySerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_summary="Get agency details",
        operation_description="Get detailed information about a specific agency.",
        tags=['Agencies'],
        responses={200: AgencyDetailSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update agency",
        operation_description="Update the information of a specific agency.",
        tags=['Agencies'],
        request_body=AgencyDetailSerializer,
        responses={200: AgencyDetailSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update agency",
        operation_description="Update specific fields of an agency.",
        tags=['Agencies'],
        request_body=AgencyDetailSerializer,
        responses={200: AgencyDetailSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete agency",
        operation_description="Remove a specific agency from the system.",
        tags=['Agencies'],
        responses={204: "No Content"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_summary="List agency emergency types",
        operation_description="Get a list of all emergency types that agencies can handle.",
        tags=['Agency Emergency Types'],
        responses={200: AgencyEmergencyTypeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create agency emergency type",
        operation_description="Associate a new emergency type with an agency.",
        tags=['Agency Emergency Types'],
        request_body=AgencyEmergencyTypeSerializer,
        responses={201: AgencyEmergencyTypeSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_summary="Get agency emergency type details",
        operation_description="Get details about a specific agency-emergency type association.",
        tags=['Agency Emergency Types'],
        responses={200: AgencyEmergencyTypeSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update agency emergency type",
        operation_description="Update an agency-emergency type association.",
        tags=['Agency Emergency Types'],
        request_body=AgencyEmergencyTypeSerializer,
        responses={200: AgencyEmergencyTypeSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update agency emergency type",
        operation_description="Update specific fields of an agency-emergency type association.",
        tags=['Agency Emergency Types'],
        request_body=AgencyEmergencyTypeSerializer,
        responses={200: AgencyEmergencyTypeSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete agency emergency type",
        operation_description="Remove an emergency type association from an agency.",
        tags=['Agency Emergency Types'],
        responses={204: "No Content"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
