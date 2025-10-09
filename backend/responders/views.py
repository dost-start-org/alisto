from rest_framework import generics, permissions
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
