from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from .models import VerificationRequest, EmergencyReport
from accounts.models import UserProfile
from .serializers import VerificationRequestCreateSerializer
import math
import logging

# Helper function for Haversine distance (in kilometers)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    dphi = math.radians(float(lat2) - float(lat1))
    dlambda = math.radians(float(lon2) - float(lon1))
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def notify_user(user_profile, message):
    # Placeholder for notification logic (email, push, etc.)
    logging.info(f"Notify {user_profile.full_name} ({user_profile.id}): {message}")


def notify_users(user_profiles, message):
    for user in user_profiles:
        notify_user(user, message)

class SendVerificationRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = VerificationRequestCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        report_id = serializer.validated_data['emergency_report_id']
        radius_km = serializer.validated_data.get('radius_km', 1.0)
        try:
            report = EmergencyReport.objects.get(report_id=report_id)
        except EmergencyReport.DoesNotExist:
            return Response({'detail': 'Emergency report not found.'}, status=404)
        # Find nearby users (excluding the reporter)
        users = UserProfile.objects.filter(
            ~Q(id=report.reported_by_id),
            status='approved',
            email_verified=True
        )
        nearby_users = []
        for user in users:
            if hasattr(user, 'latitude') and hasattr(user, 'longitude') and user.latitude and user.longitude:
                dist = haversine(report.latitude, report.longitude, user.latitude, user.longitude)
                if dist <= radius_km:
                    nearby_users.append(user)
        if not nearby_users:
            return Response({'detail': 'No nearby users found.'}, status=200)
        # Create VerificationRequest
        vreq = VerificationRequest.objects.create(emergency_report=report)
        vreq.targeted_users.set(nearby_users)
        vreq.save()
        # Notify targeted users
        notify_users(nearby_users, f"You have a new verification request for emergency report {report.report_id}.")
        logging.info(f"VerificationRequest {vreq.id} sent to users {[u.id for u in nearby_users]}")
        return Response({'verification_request_id': vreq.id, 'targeted_user_ids': [u.id for u in nearby_users]}, status=201)

class VerificationResponseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from .serializers import VerificationResponseSerializer
        serializer = VerificationResponseSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        vreq_id = serializer.validated_data['verification_request_id']
        response_val = serializer.validated_data['response']
        vreq = VerificationRequest.objects.get(id=vreq_id)
        user = request.user.profile
        # Prevent duplicate responses
        if vreq.responses.filter(user=user).exists():
            return Response({'detail': 'User has already responded.'}, status=400)
        vresp = vreq.responses.create(user=user, response=response_val)
        # Notify user of successful response
        notify_user(user, f"Your response to verification request {vreq.id} has been recorded.")
        logging.info(f"User {user.id} responded {response_val} to VerificationRequest {vreq.id}")
        # Optionally, update status or trigger analytics here
        return Response({'detail': 'Response recorded.'}, status=201)

class UpdateVerificationStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        vreq_id = request.data.get('verification_request_id')
        try:
            vreq = VerificationRequest.objects.get(id=vreq_id)
        except VerificationRequest.DoesNotExist:
            return Response({'detail': 'Verification request not found.'}, status=404)
        status_str, yes_ratio = vreq.get_verification_status()
        # Optionally update EmergencyReport or VerificationRequest status
        vreq.status = 'Completed'
        vreq.save()
        # Update EmergencyReport with verification status (custom field or notes)
        report = vreq.emergency_report
        report.resolution_notes += f"\nVerification status: {status_str} ({yes_ratio*100:.0f}% yes)"
        report.save()
        # Notify reporter and responders of verification status
        notify_user(report.reported_by, f"Verification status for your report {report.report_id}: {status_str}")
        logging.info(f"Verification status for report {report.report_id}: {status_str} ({yes_ratio*100:.0f}% yes)")
        return Response({'verification_status': status_str, 'yes_ratio': yes_ratio}, status=200)

# Create your views here.
