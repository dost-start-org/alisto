import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import UserEmergencyContact

User = get_user_model()


class UserEmergencyContactTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.user1 = User.objects.create_user(
            email="user1@example.com", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", password="testpass123"
        )

        # Create sample contacts for user1
        self.contact1 = UserEmergencyContact.objects.create(
            user=self.user1,
            name="Mom",
            phone_number="09171234567",
            relationship="Mother"
        )
        self.contact2 = UserEmergencyContact.objects.create(
            user=self.user1,
            name="Dad",
            phone_number="09991234567",
            relationship="Father"
        )

        # URLs
        self.list_url = reverse("user-contact-list-create")
        self.detail_url = lambda pk: reverse("user-contact-detail", args=[pk])

    def test_auth_required(self):
        """Unauthenticated users cannot access the list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_own_contacts(self):
        """Authenticated user should only see their own contacts."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(c["name"] in ["Mom", "Dad"] for c in response.data))

    def test_create_contact(self):
        """User can create a new personal emergency contact."""
        self.client.force_authenticate(user=self.user1)
        data = {
            "name": "Brother",
            "phone_number": "09170000000",
            "relationship": "Sibling"
        }
        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserEmergencyContact.objects.filter(user=self.user1).count(), 3)
        self.assertEqual(response.data["name"], "Brother")

    def test_retrieve_own_contact(self):
        """User can retrieve details of their own contact."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.detail_url(self.contact1.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Mom")

    def test_retrieve_other_user_contact_forbidden(self):
        """User cannot access another user's contact."""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.detail_url(self.contact1.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_contact(self):
        """User can update their own contact."""
        self.client.force_authenticate(user=self.user1)
        data = {"name": "Updated Mom", "relationship": "Mother"}

        response = self.client.patch(self.detail_url(self.contact1.id), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.contact1.refresh_from_db()
        self.assertEqual(self.contact1.name, "Updated Mom")

    def test_delete_own_contact(self):
        """User can delete their own contact."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.detail_url(self.contact2.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserEmergencyContact.objects.filter(id=self.contact2.id).exists())
