from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema
from .models import Responder
from .serializers import ResponderSerializer, ResponderCreateSerializer

class ResponderList(generics.ListCreateAPIView):
    """
    list:
    Get a list of all responders registered in the system.

    create:
    Register a new responder in the system.
    """
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ResponderCreateSerializer
        return ResponderSerializer

    def perform_create(self, serializer):
        serializer.save()

    @swagger_auto_schema(
        operation_summary="List responders",
        operation_description="Get a list of all responders registered in the system.",
        tags=['Responders'],
        responses={
            200: ResponderSerializer(many=True)
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create responder",
        operation_description="Register a new responder in the system.",
        tags=['Responders'],
        request_body=ResponderCreateSerializer,
        responses={
            201: ResponderSerializer
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ResponderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    retrieve:
    Get detailed information about a specific responder.

    update:
    Update the information of a specific responder.

    partial_update:
    Update specific fields of a responder.

    destroy:
    Remove a specific responder from the system.
    """
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get responder details",
        operation_description="Get detailed information about a specific responder.",
        tags=['Responders'],
        responses={
            200: ResponderSerializer
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update responder",
        operation_description="Update the information of a specific responder.",
        tags=['Responders'],
        request_body=ResponderSerializer,
        responses={
            200: ResponderSerializer
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update responder",
        operation_description="Update specific fields of a responder.",
        tags=['Responders'],
        request_body=ResponderSerializer,
        responses={
            200: ResponderSerializer
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete responder",
        operation_description="Remove a specific responder from the system.",
        tags=['Responders'],
        responses={
            204: "No Content"
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
