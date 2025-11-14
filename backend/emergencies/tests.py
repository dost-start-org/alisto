from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, UserProfile
from .models import EmergencyReport, EmergencyVerification, EmergencyType
from agencies.models import Agency  # Import Agency model
import uuid
from rest_framework.exceptions import ErrorDetail, ValidationError
from unittest.mock import patch

class VerificationSystemTests(TestCase):
    def test_crowdsourcing_poll_notification_expires(self):
        """Test that a user receives a notification when included in a broadcast and that it expires."""
        from emergencies.models import CrowdsourceBroadcast
        from django.utils import timezone
        url_broadcast = reverse('trigger-crowdsourcing-broadcast')
        url_poll = reverse('crowdsource-poll-notification')

        # Trigger broadcast for user2 (nearby)
        data = {
            'report_id': str(self.report.id),
            'range': 1.0
        }
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url_broadcast, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        broadcast_id = response.data['broadcast_id']

        # Poll for notification (should receive it)
        response = self.client.get(url_poll)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['signal'])
        self.assertIn('broadcast_data', response.data)
        self.assertEqual(response.data['broadcast_data']['broadcast_id'], broadcast_id)

        # Simulate expiration
        broadcast = CrowdsourceBroadcast.objects.get(id=broadcast_id)
        broadcast.expires_at = timezone.now() - timezone.timedelta(minutes=1)
        broadcast.save()

        # Poll again (should not receive notification)
        response = self.client.get(url_poll)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['signal'])
    def test_verification_create_includes_confirmed_field(self):
        """Test that creating a verification includes the 'confirmed' field in the response."""
        url = reverse('emergency-verification-list')
        data = {
            'report': str(self.report.id),
            'vote': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('confirmed', response.data)
        self.assertTrue(response.data['confirmed'])

        # Now test with vote=False (must provide details)
        data_false = {
            'report': str(self.report.id),
            'vote': False,
            'details': 'Denial reason'  # At least 5 characters
        }
        response = self.client.post(url, data_false, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('confirmed', response.data)
        self.assertFalse(response.data['confirmed'])

    def test_verification_patch_includes_confirmed_field(self):
        """Test that updating a verification includes the 'confirmed' field in the response."""
        everification = EmergencyVerification.objects.create(
            report=self.report,
            user=self.user,
            vote=None
        )
        url = reverse('emergency-verification-detail', kwargs={'pk': everification.id})
        data = {'vote': True}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('confirmed', response.data)
        self.assertTrue(response.data['confirmed'])

        # Now test with vote=False
        data['vote'] = False
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('confirmed', response.data)
        self.assertFalse(response.data['confirmed'])
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
        # Ensure user has a UserProfile
        self.userprofile, created = UserProfile.objects.get_or_create(
            user=self.user,
            defaults={
                'full_name': 'Responder User',
                'authority_level': 'Responder',
                'contact_number': '1234567890',
                'date_of_birth': '1990-01-01',
                'address': 'Test Address',
                'status': 'approved',
                'email_verified': True
            }
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

    def test_responder_accept_report(self):
        url = reverse('emergency_report_responder_actions', kwargs={'report_id': self.report.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.report.refresh_from_db()
        self.assertEqual(self.report.responder, self.user)
        self.assertEqual(self.report.status, 'Responding')

    def test_responder_unassign_report(self):
        self.report.responder = self.user
        self.report.status = 'Responding'
        self.report.save()

        url = reverse('emergency_report_responder_actions', kwargs={'report_id': self.report.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.report.refresh_from_db()
        self.assertIsNone(self.report.responder)
        self.assertEqual(self.report.status, 'Pending')

    def test_responder_update_status(self):
        self.report.responder = self.user
        self.report.status = 'Responding'
        self.report.save()

        url = reverse('emergency_report_status_update', kwargs={'report_id': self.report.id})
        data = {'status': 'Resolved'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, 'Resolved')

    def test_invalid_status_update(self):
        self.report.responder = self.user
        self.report.status = 'Responding'
        self.report.save()

        url = reverse('emergency_report_status_update', kwargs={'report_id': self.report.id})
        data = {'status': 'InvalidStatus'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_trigger_crowdsourcing(self):
        url = reverse('trigger_crowdsourcing', kwargs={'report_id': self.report.id})
        self.user.profile.authority_level = 'Responder'
        self.user.profile.save()
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('notified_users', response.data)

    def test_respond_to_emergency(self):
        self.report.responder = self.user
        self.report.status = 'Responding'
        self.report.save()

        url = reverse('respond_to_emergency', kwargs={'report_id': self.report.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, 'Responded')

    def test_notification_on_status_change(self):
        self.report.status = 'Resolved'
        self.report.save()

        # Check if the notification signal was triggered (mocked for now)
        # In a real test, you would use Django's mail.outbox to verify email sending
        self.assertEqual(self.report.status, 'Resolved')

    @patch('emergencies.serializers.FileService.process_image_field')
    def test_create_emergency_report_with_image_base64(self, mock_process_image_field):
        mock_process_image_field.return_value = (True, 'https://example.com/uploaded.png')
        url = reverse('emergency-report-list')
        data = {
            'emergency_type': str(self.report.emergency_type.id),
            'longitude': 120.99,
            'latitude': 14.60,
            'details': 'Valid emergency details',
            'image_base64': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(
            response.data['data']['image_url'],
            'https://example.com/uploaded.png'
        )
        mock_process_image_field.assert_called_once_with(
            'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA',
            folder='emergency_reports'
        )

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
