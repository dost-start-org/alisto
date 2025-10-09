from rest_framework import generics, permissions
from .models import EmergencyContact, ContactRedirection
from .serializers import (
    EmergencyContactSerializer, EmergencyContactDetailSerializer,
    ContactRedirectionSerializer
)

class EmergencyContactList(generics.ListCreateAPIView):
    """
    list:
    Get a list of all emergency contacts in the system.

    create:
    Add a new emergency contact to the system.
    """
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EmergencyContactDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    retrieve:
    Get detailed information about a specific emergency contact.

    update:
    Update the information of a specific emergency contact.

    partial_update:
    Update specific fields of an emergency contact.

    destroy:
    Remove a specific emergency contact from the system.
    """
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ContactRedirectionList(generics.ListCreateAPIView):
    """
    list:
    Get a list of all contact redirections for emergency types.

    create:
    Create a new contact redirection for an emergency type.
    """
    queryset = ContactRedirection.objects.all()
    serializer_class = ContactRedirectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ContactRedirectionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    retrieve:
    Get details about a specific contact redirection.

    update:
    Update a contact redirection.

    partial_update:
    Update specific fields of a contact redirection.

    destroy:
    Remove a contact redirection.
    """
    queryset = ContactRedirection.objects.all()
    serializer_class = ContactRedirectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
