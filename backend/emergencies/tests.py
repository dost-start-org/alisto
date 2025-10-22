from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, UserProfile
from .models import EmergencyReport, EmergencyVerification, EmergencyType
from agencies.models import Agency  # Import Agency model
import uuid
from rest_framework.exceptions import ErrorDetail, ValidationError

class VerificationSystemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user1@example.com', password='pass')
        self.profile = UserProfile.objects.create(
            user=self.user,
            full_name='User One',
            authority_level='User',
            contact_number='123',
            date_of_birth='2000-01-01',
            address='Test',
            status='approved',
            email_verified=True
        )
        self.report = EmergencyReport.objects.create(
            emergency_type=EmergencyType.objects.create(name='Fire', icon_type='fire-icon'),
            user=self.user,
            longitude=120.9842,
            latitude=14.5995,
            details='Test emergency report',
            status='Pending'
        )
        self.profile.latitude = 14.5995
        self.profile.longitude = 120.9842
        self.profile.save()
        # Add a second user nearby to ensure the endpoint finds a target
        self.user2 = User.objects.create_user(email='user2@example.com', password='pass')
        self.profile2 = UserProfile.objects.create(
            user=self.user2,
            full_name='User Two',
            authority_level='User',
            contact_number='456',
            date_of_birth='2000-01-01',
            address='Test',
            status='approved',
            email_verified=True,
            latitude=14.5996,
            longitude=120.9843
        )
        self.client.force_authenticate(user=self.user)

    def test_verification_response(self):
        # Create emergency verification
        everification = EmergencyVerification.objects.create(
            report=self.report,
            user=self.user,
            vote=None
        )
        url = reverse('emergency-verification-detail', kwargs={'pk': everification.id})
        data = {'vote': True}
        response = self.client.patch(url, data, format='json')
        print("Response status code:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(EmergencyVerification.objects.filter(id=everification.id, vote=True).exists())

    def test_update_verification_status(self):
        everification = EmergencyVerification.objects.create(
            report=self.report,
            user=self.user,
            vote=True
        )
        url = reverse('mark-report-as-verified')
        data = {'report_id': str(self.report.id)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.report.verification_status, 'Verified')

    def test_trigger_crowdsourcing_broadcast(self):
        url = reverse('trigger-crowdsourcing-broadcast')
        data = {
            'report_id': str(self.report.id),
            'range': 1.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('notified_agencies', response.data)

    def test_trigger_crowdsourcing_broadcast_excludes_out_of_range_users_and_notifies_agencies(self):
        user_out_of_range = User.objects.create_user(email='user3@example.com', password='pass')
        profile_out_of_range = UserProfile.objects.create(
            user=user_out_of_range,
            full_name='User Three',
            authority_level='User',
            contact_number='789',
            date_of_birth='2000-01-01',
            address='Far Away',
            status='approved',
            email_verified=True,
            latitude=15.0000,
            longitude=121.0000
        )

        url = reverse('trigger-crowdsourcing-broadcast')
        data = {
            'report_id': str(self.report.id),
            'range': 1.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('notified_agencies', response.data)
        self.assertNotIn(user_out_of_range.id, response.data['users'])

class EnhancedVerificationSystemTests(VerificationSystemTests):
    def test_verification_response_invalid_vote(self):
        """Test invalid vote value in verification response."""
        everification = EmergencyVerification.objects.create(
            report=self.report,
            user=self.user,
            vote=None
        )
        url = reverse('emergency-verification-detail', kwargs={'pk': everification.id})
        data = {'vote': 'invalid_value'}  # Invalid vote value
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('vote', response.data)
        self.assertIn('value must be either True, False, or None', str(response.data['vote']))

    def test_trigger_crowdsourcing_broadcast_invalid_report_id(self):
        """Test crowdsourcing broadcast with an invalid report ID."""
        url = reverse('trigger-crowdsourcing-broadcast')
        data = {
            'report_id': str(uuid.uuid4()),  # Non-existent report ID
            'range': 1.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'No EmergencyReport matches the given query.')

    def test_trigger_crowdsourcing_broadcast_zero_range(self):
        """Test crowdsourcing broadcast with a range of 0 km."""
        url = reverse('trigger-crowdsourcing-broadcast')
        data = {
            'report_id': str(self.report.id),
            'range': 0.0  # Zero range
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['users']), 0)  # No users should be within range
        self.assertEqual(len(response.data['notified_agencies']), 0)  # No agencies should be notified

    def test_trigger_crowdsourcing_broadcast_large_range(self):
        """Test crowdsourcing broadcast with a very large range."""
        url = reverse('trigger-crowdsourcing-broadcast')
        data = {
            'report_id': str(self.report.id),
            'range': 10000.0  # Very large range
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate that users are within the specified range
        for user_id in response.data['users']:
            user_profile = UserProfile.objects.get(user_id=user_id)
            distance = self.calculate_distance(
                self.report.latitude, self.report.longitude,
                user_profile.latitude, user_profile.longitude
            )
            self.assertLessEqual(distance, 10000.0, f"User {user_id} is out of range.")

        # Validate that agencies are within the specified range
        for agency in response.data['notified_agencies']:
            agency_obj = Agency.objects.get(name=agency['agency_name'])
            distance = self.calculate_distance(
                self.report.latitude, self.report.longitude,
                agency_obj.latitude, agency_obj.longitude
            )
            self.assertLessEqual(distance, 10000.0, f"Agency {agency['agency_name']} is out of range.")

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Helper method to calculate the distance between two coordinates."""
        from math import radians, sin, cos, sqrt, atan2
        R = 6371  # Radius of the Earth in kilometers
        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])  # Convert to float
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def test_unauthorized_access(self):
        """Test unauthorized access to endpoints."""
        self.client.force_authenticate(user=None)  # Unauthenticate the client

        # Test verification response
        everification = EmergencyVerification.objects.create(
            report=self.report,
            user=self.user,
            vote=None
        )
        url = reverse('emergency-verification-detail', kwargs={'pk': everification.id})
        response = self.client.patch(url, {'vote': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test crowdsourcing broadcast
        url = reverse('trigger-crowdsourcing-broadcast')
        response = self.client.post(url, {'report_id': str(self.report.id), 'range': 1.0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
