from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, UserProfile
from .models import EmergencyReport, VerificationRequest, VerificationResponse
import uuid

class VerificationSystemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user1@example.com', password='pass')
        self.profile = UserProfile.objects.create(user=self.user, full_name='User One', authority_level='User', contact_number='123', date_of_birth='2000-01-01', address='Test', status='approved', email_verified=True)
        self.report = EmergencyReport.objects.create(
            report_id=uuid.uuid4(),
            reported_by=self.profile,
            report_type='Fire',
            latitude=14.5995,
            longitude=120.9842,
            status='Pending'
        )
        self.profile.latitude = 14.5995
        self.profile.longitude = 120.9842
        self.profile.save()
        # Add a second user nearby to ensure the endpoint finds a target
        self.user2 = User.objects.create_user(email='user2@example.com', password='pass')
        self.profile2 = UserProfile.objects.create(user=self.user2, full_name='User Two', authority_level='User', contact_number='456', date_of_birth='2000-01-01', address='Test', status='approved', email_verified=True, latitude=14.5996, longitude=120.9843)
        self.client.force_authenticate(user=self.user)

    def test_send_verification_request(self):
        url = reverse('send_verification_request')
        data = {'emergency_report_id': str(self.report.report_id), 'radius_km': 1.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('verification_request_id', response.data)

    def test_verification_response(self):
        # Create verification request
        vreq = VerificationRequest.objects.create(emergency_report=self.report)
        vreq.targeted_users.add(self.profile)
        vreq.save()
        url = reverse('verification_response')
        data = {'verification_request_id': vreq.id, 'response': 'Yes'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(VerificationResponse.objects.filter(verification_request=vreq, user=self.profile).exists())

    def test_update_verification_status(self):
        vreq = VerificationRequest.objects.create(emergency_report=self.report)
        vreq.targeted_users.add(self.profile)
        vreq.save()
        VerificationResponse.objects.create(verification_request=vreq, user=self.profile, response='Yes')
        url = reverse('update_verification_status')
        data = {'verification_request_id': vreq.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('verification_status', response.data)
