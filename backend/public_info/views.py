from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema
from .models import EmergencyContact, ContactRedirection, UserEmergencyContact
from .serializers import (
    EmergencyContactSerializer, EmergencyContactDetailSerializer,
    ContactRedirectionSerializer, UserEmergencyContactSerializer
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

    @swagger_auto_schema(
        operation_summary="List emergency contacts",
        operation_description="Get a list of all emergency contacts in the system.",
        tags=['Emergency Contacts'],
        responses={200: EmergencyContactSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create emergency contact",
        operation_description="Add a new emergency contact to the system.",
        tags=['Emergency Contacts'],
        request_body=EmergencyContactSerializer,
        responses={201: EmergencyContactSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_summary="Get emergency contact details",
        operation_description="Get detailed information about a specific emergency contact.",
        tags=['Emergency Contacts'],
        responses={200: EmergencyContactDetailSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update emergency contact",
        operation_description="Update the information of a specific emergency contact.",
        tags=['Emergency Contacts'],
        request_body=EmergencyContactDetailSerializer,
        responses={200: EmergencyContactDetailSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update emergency contact",
        operation_description="Update specific fields of an emergency contact.",
        tags=['Emergency Contacts'],
        request_body=EmergencyContactDetailSerializer,
        responses={200: EmergencyContactDetailSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete emergency contact",
        operation_description="Remove a specific emergency contact from the system.",
        tags=['Emergency Contacts'],
        responses={204: "No Content"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_summary="List contact redirections",
        operation_description="Get a list of all contact redirections for emergency types.",
        tags=['Contact Redirections'],
        responses={200: ContactRedirectionSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create contact redirection",
        operation_description="Create a new contact redirection for an emergency type.",
        tags=['Contact Redirections'],
        request_body=ContactRedirectionSerializer,
        responses={201: ContactRedirectionSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_summary="Get contact redirection details",
        operation_description="Get details about a specific contact redirection.",
        tags=['Contact Redirections'],
        responses={200: ContactRedirectionSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update contact redirection",
        operation_description="Update a contact redirection.",
        tags=['Contact Redirections'],
        request_body=ContactRedirectionSerializer,
        responses={200: ContactRedirectionSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update contact redirection",
        operation_description="Update specific fields of a contact redirection.",
        tags=['Contact Redirections'],
        request_body=ContactRedirectionSerializer,
        responses={200: ContactRedirectionSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete contact redirection",
        operation_description="Remove a contact redirection.",
        tags=['Contact Redirections'],
        responses={204: "No Content"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class UserEmergencyContactListCreateView(generics.ListCreateAPIView):
    """
    list:
    Get a list of the user's personal emergency contacts.

    create:
    Add a new personal emergency contact for the logged-in user.
    """
    serializer_class = UserEmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return contacts belonging to the logged-in user
        return UserEmergencyContact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List user's emergency contacts",
        operation_description="Retrieve a list of the logged-in user's personal emergency contacts.",
        tags=['User Emergency Contacts'],
        responses={200: UserEmergencyContactSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create user emergency contact",
        operation_description="Add a new emergency contact for the logged-in user.",
        tags=['User Emergency Contacts'],
        request_body=UserEmergencyContactSerializer,
        responses={201: UserEmergencyContactSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserEmergencyContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    retrieve:
    Get detailed information about a user's specific emergency contact.

    update:
    Update a user's emergency contact details.

    partial_update:
    Partially update a user's emergency contact.

    destroy:
    Delete a user's emergency contact.
    """
    serializer_class = UserEmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow access to the user's own contacts
        return UserEmergencyContact.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Get user emergency contact details",
        operation_description="Retrieve details about a specific emergency contact belonging to the logged-in user.",
        tags=['User Emergency Contacts'],
        responses={200: UserEmergencyContactSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update user emergency contact",
        operation_description="Update the details of a specific emergency contact belonging to the logged-in user.",
        tags=['User Emergency Contacts'],
        request_body=UserEmergencyContactSerializer,
        responses={200: UserEmergencyContactSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update user emergency contact",
        operation_description="Partially update a specific emergency contact belonging to the logged-in user.",
        tags=['User Emergency Contacts'],
        request_body=UserEmergencyContactSerializer,
        responses={200: UserEmergencyContactSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete user emergency contact",
        operation_description="Remove a specific emergency contact belonging to the logged-in user.",
        tags=['User Emergency Contacts'],
        responses={204: "No Content"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
