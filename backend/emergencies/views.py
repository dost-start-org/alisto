from rest_framework import generics, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.html import escape
from rest_framework.exceptions import ValidationError
import bleach
import math
from accounts.models import User, UserProfile
from .models import EmergencyType, EmergencyReport, EmergencyVerification, UserEvaluation
from .serializers import (
    EmergencyTypeSerializer,
    EmergencyReportSerializer,
    EmergencyVerificationSerializer,
    UserEvaluationSerializer
)
from agencies.models import Agency, AgencyEmergencyType
from django.core.mail import send_mail

class EmergencyTypeList(generics.ListCreateAPIView):
    """
    list:
    Return a list of all emergency types.

    create:
    Create a new emergency type.
    """
    queryset = EmergencyType.objects.all()
    serializer_class = EmergencyTypeSerializer

    @swagger_auto_schema(
        operation_description="List all emergency types",
        tags=['Emergency Types'],
        responses={
            200: EmergencyTypeSerializer(many=True)
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new emergency type",
        tags=['Emergency Types'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'icon_type'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the emergency type'),
                'icon_type': openapi.Schema(type=openapi.TYPE_STRING, description='Icon identifier for this emergency type')
            }
        ),
        responses={
            201: EmergencyTypeSerializer()
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class EmergencyTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyType.objects.all()
    serializer_class = EmergencyTypeSerializer

    @swagger_auto_schema(
        operation_description="Get details of an emergency type",
        tags=['Emergency Types'],
        responses={
            200: EmergencyTypeSerializer(),
            404: "Emergency type not found"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an emergency type",
        tags=['Emergency Types'],
        request_body=EmergencyTypeSerializer,
        responses={
            200: EmergencyTypeSerializer(),
            404: "Emergency type not found"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update an emergency type",
        tags=['Emergency Types'],
        request_body=EmergencyTypeSerializer,
        responses={
            200: EmergencyTypeSerializer(),
            404: "Emergency type not found"
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete an emergency type",
        tags=['Emergency Types'],
        responses={
            204: "No Content",
            404: "Emergency type not found"
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class EmergencyReportList(generics.ListCreateAPIView):
    queryset = EmergencyReport.objects.all()
    serializer_class = EmergencyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def sanitize_input(self, data):
        """Sanitize input data to prevent XSS and other injection attacks"""
        if 'details' in data:
            # Escape HTML and allow only basic formatting
            data['details'] = bleach.clean(
                data['details'],
                tags=['b', 'i', 'u'],  # Allow only basic formatting
                strip=True
            )
        return data

    def create(self, request, *args, **kwargs):
        # Sanitize input before validation
        sanitized_data = self.sanitize_input(request.data.copy())
        
        # Validate data
        serializer = self.get_serializer(data=sanitized_data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': e.detail
            }, status=400)

        # Save with current user
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response({
            'status': 'success',
            'message': 'Emergency report created successfully',
            'data': serializer.data
        }, status=201, headers=headers)

    @swagger_auto_schema(
        operation_description="List all emergency reports",
        tags=['Emergency Reports'],
        responses={
            200: EmergencyReportSerializer(many=True),
            401: "Authentication required"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new emergency report",
        tags=['Emergency Reports'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['emergency_type', 'longitude', 'latitude'],
            properties={
                'emergency_type': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='ID of the emergency type'),
                'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='Longitude of the emergency location'),
                'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description='Latitude of the emergency location'),
                'details': openapi.Schema(type=openapi.TYPE_STRING, description='Additional details about the emergency'),
                'image_url': openapi.Schema(type=openapi.TYPE_STRING, description='Base64 encoded image string (with or without data URL prefix) or an image URL')
            }
        ),
        responses={
            201: EmergencyReportSerializer(),
            401: "Authentication required"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EmergencyReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyReport.objects.all()
    serializer_class = EmergencyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get details of an emergency report",
        tags=['Emergency Reports'],
        responses={
            200: EmergencyReportSerializer(),
            401: "Authentication required",
            404: "Emergency report not found"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an emergency report",
        tags=['Emergency Reports'],
        request_body=EmergencyReportSerializer,
        responses={
            200: EmergencyReportSerializer(),
            401: "Authentication required",
            404: "Emergency report not found"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update an emergency report",
        tags=['Emergency Reports'],
        request_body=EmergencyReportSerializer,
        responses={
            200: EmergencyReportSerializer(),
            401: "Authentication required",
            404: "Emergency report not found"
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete an emergency report",
        tags=['Emergency Reports'],
        responses={
            204: "No Content",
            401: "Authentication required",
            404: "Emergency report not found"
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class EmergencyVerificationList(generics.ListCreateAPIView):
    queryset = EmergencyVerification.objects.all()
    serializer_class = EmergencyVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all emergency verifications",
        tags=['Emergency Verifications'],
        responses={
            200: EmergencyVerificationSerializer(many=True)
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new emergency verification. Details are required and must be at least 5 characters when denying a report (vote=false).",
        tags=['Emergency Verifications'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['report', 'vote'],
            properties={
                'report': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='ID of the emergency report to verify'),
                'vote': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='True if verifying the emergency, False if denying'),
                'details': openapi.Schema(type=openapi.TYPE_STRING, description='Additional details about the verification. Required when vote is False, must be at least 5 characters.'),
                'image_url': openapi.Schema(type=openapi.TYPE_STRING, description='Base64 encoded image string (with or without data URL prefix) or an image URL')
            }
        ),
        responses={
            201: EmergencyVerificationSerializer(),
            400: "Validation error - details required for denial or too short",
            401: "Authentication required"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EmergencyVerificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyVerification.objects.all()
    serializer_class = EmergencyVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get details of an emergency verification",
        tags=['Emergency Verifications'],
        responses={
            200: EmergencyVerificationSerializer(),
            401: "Authentication required",
            404: "Emergency verification not found"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an emergency verification",
        tags=['Emergency Verifications'],
        request_body=EmergencyVerificationSerializer,
        responses={
            200: EmergencyVerificationSerializer(),
            401: "Authentication required",
            404: "Emergency verification not found"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update an emergency verification",
        tags=['Emergency Verifications'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'vote': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='True if verifying the emergency, False if denying')
            }
        ),
        responses={
            200: EmergencyVerificationSerializer(),
            400: "Validation error",
            404: "Emergency verification not found"
        }
    )
    def patch(self, request, *args, **kwargs):
        verification = self.get_object()
        vote = request.data.get('vote')

        # Validate the vote value
        if vote not in [True, False, None]:
            return Response(
                {'vote': ['“{}” value must be either True, False, or None.'.format(vote)]},
                status=status.HTTP_400_BAD_REQUEST
            )

        if vote is not None:
            verification.vote = vote
            verification.save()

        serializer = self.get_serializer(verification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete an emergency verification",
        tags=['Emergency Verifications'],
        responses={
            204: "No Content",
            401: "Authentication required",
            404: "Emergency verification not found"
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class UserEvaluationList(generics.ListCreateAPIView):
    queryset = UserEvaluation.objects.all()
    serializer_class = UserEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all user evaluations",
        tags=['User Evaluations'],
        responses={
            200: UserEvaluationSerializer(many=True)
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new user evaluation",
        tags=['User Evaluations'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['report', 'stars', 'did_app_guide_clearly', 'completion_speed', 'confidence_level'],
            properties={
                'report': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='ID of the emergency report to evaluate'),
                'stars': openapi.Schema(type=openapi.TYPE_INTEGER, description='Rating from 1 to 5 stars'),
                'did_app_guide_clearly': openapi.Schema(type=openapi.TYPE_STRING, enum=['Yes', 'Somewhat', 'No'], description='Whether the app provided clear guidance'),
                'completion_speed': openapi.Schema(type=openapi.TYPE_STRING, enum=['Very fast', 'Acceptable', 'Too slow'], description='How fast the emergency was handled'),
                'confidence_level': openapi.Schema(type=openapi.TYPE_STRING, enum=['Not confident', 'Neutral', 'Very confident'], description='User confidence in the response'),
                'improvement_suggestion': openapi.Schema(type=openapi.TYPE_STRING, description='Suggestions for improvement')
            }
        ),
        responses={
            201: UserEvaluationSerializer(),
            401: "Authentication required"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserEvaluationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserEvaluation.objects.all()
    serializer_class = UserEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get details of a user evaluation",
        tags=['User Evaluations'],
        responses={
            200: UserEvaluationSerializer(),
            401: "Authentication required",
            404: "User evaluation not found"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a user evaluation",
        tags=['User Evaluations'],
        request_body=UserEvaluationSerializer,
        responses={
            200: UserEvaluationSerializer(),
            401: "Authentication required",
            404: "User evaluation not found"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a user evaluation",
        tags=['User Evaluations'],
        request_body=UserEvaluationSerializer,
        responses={
            200: UserEvaluationSerializer(),
            401: "Authentication required",
            404: "User evaluation not found"
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a user evaluation",
        tags=['User Evaluations'],
        responses={
            204: "No Content",
            401: "Authentication required",
            404: "User evaluation not found"
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class TriggerCrowdsourcingBroadcast(APIView):
    """
    Endpoint for responders to trigger a crowdsourcing broadcast within a specific range.
    """
    permission_classes = [permissions.IsAuthenticated]

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great-circle distance between two points on the Earth using the Haversine formula.
        """
        # Convert all inputs to float to handle type mismatches
        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])

        # Check if the points are the same (distance is 0)
        if lat1 == lat2 and lon1 == lon1:
            print(f"Points are the same: ({lat1}, {lon1})")
            return 0.0

        R = 6371  # Radius of the Earth in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        # Treat very small distances as zero
        if distance < 0.1:  # Adjusted threshold for very small distances
            print(f"Distance ({distance} km) is considered zero.")
            return 0.0

        print(f"Calculated distance: {distance} km between ({lat1}, {lon1}) and ({lat2}, {lon2})")
        return distance

    @swagger_auto_schema(
        operation_description="Trigger a crowdsourcing broadcast for an emergency report within a specific range.",
        tags=['Crowdsourcing'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['report_id', 'range'],
            properties={
                'report_id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='ID of the emergency report'),
                'range': openapi.Schema(type=openapi.TYPE_NUMBER, description='Range in kilometers for the broadcast')
            }
        ),
        responses={
            200: "Broadcast triggered successfully",
            404: "Emergency report not found",
            401: "Authentication required"
        }
    )
    def post(self, request):
        report_id = request.data.get('report_id')
        broadcast_range = request.data.get('range', 5)  # Default range is 5 km

        # Validate the emergency report
        report = get_object_or_404(EmergencyReport, id=report_id)
        report_lat, report_lon = report.latitude, report.longitude

        # Filter all user profiles within the specified range
        user_profiles = UserProfile.objects.filter(status='approved')
        users_within_range = []
        # Exclude users when the range is explicitly set to 0 km
        if broadcast_range == 0:
            users_within_range = []
        else:
            for profile in user_profiles:
                distance = self.haversine_distance(report_lat, report_lon, profile.latitude, profile.longitude)
                print(f"User {profile.user.id}: Distance = {distance} km")
                if distance <= broadcast_range:
                    users_within_range.append(profile.user)

        # Filter relevant agencies by emergency type and proximity
        relevant_agencies = Agency.objects.filter(
            agencyemergencytype__emergency_type=report.emergency_type
        )
        agencies_within_range = []
        for agency in relevant_agencies:
            distance = self.haversine_distance(report_lat, report_lon, agency.latitude, agency.longitude)
            print(f"Agency {agency.name}: Distance = {distance} km")
            if distance <= broadcast_range:
                agencies_within_range.append(agency)

        # Notify agencies (e.g., via their hotline numbers)
        agency_notifications = [
            {
                "agency_name": agency.name,
                "hotline_number": agency.hotline_number
            }
            for agency in agencies_within_range
        ]

        # Logic to trigger broadcast (e.g., WebSocket notification)
        user_ids = [user.id for user in users_within_range]

        print(f"Users within range: {user_ids}")
        print(f"Notified agencies: {agency_notifications}")

        return Response({
            "message": "Broadcast triggered successfully.",
            "users": user_ids,
            "notified_agencies": agency_notifications
        }, status=status.HTTP_200_OK)

class MarkReportAsVerified(APIView):
    """
    Endpoint for responders to manually mark a report as verified.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Manually mark an emergency report as verified.",
        tags=['Crowdsourcing'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['report_id'],
            properties={
                'report_id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='ID of the emergency report')
            }
        ),
        responses={
            200: "Report marked as verified",
            404: "Emergency report not found",
            401: "Authentication required"
        }
    )
    def post(self, request):
        report_id = request.data.get('report_id')
        report = get_object_or_404(EmergencyReport, id=report_id)
        report.verification_status = 'Verified'
        report.save()
        return Response({"message": "Report marked as verified."}, status=status.HTTP_200_OK)

class EmergencyReportResponderActions(APIView):
    """
    API view for responders to accept or reject emergency reports.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, report_id):
        report = get_object_or_404(EmergencyReport, id=report_id)

        if report.responder is not None:
            return Response({
                'status': 'error',
                'message': 'This report has already been assigned to another responder.'
            }, status=status.HTTP_400_BAD_REQUEST)

        report.responder = request.user
        report.status = 'Responding'
        report.save()

        return Response({
            'status': 'success',
            'message': 'You have been assigned to this emergency report.',
            'report_id': report.id
        }, status=status.HTTP_200_OK)

    def delete(self, request, report_id):
        report = get_object_or_404(EmergencyReport, id=report_id, responder=request.user)

        report.responder = None
        report.status = 'Pending'
        report.save()

        return Response({
            'status': 'success',
            'message': 'You have unassigned yourself from this emergency report.',
            'report_id': report.id
        }, status=status.HTTP_200_OK)

class EmergencyReportStatusUpdate(APIView):
    """
    API view for responders to update the status of an emergency report.
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, report_id):
        report = get_object_or_404(EmergencyReport, id=report_id, responder=request.user)

        new_status = request.data.get('status')
        if new_status not in dict(EmergencyReport.STATUS_CHOICES):
            return Response({
                'status': 'error',
                'message': 'Invalid status value.'
            }, status=status.HTTP_400_BAD_REQUEST)

        report.status = new_status
        report.save()

        return Response({
            'status': 'success',
            'message': f'Report status updated to {new_status}.',
            'report_id': report.id
        }, status=status.HTTP_200_OK)

class TriggerCrowdsourcing(APIView):
    """
    API view for responders to trigger a crowdsourcing verification request.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, report_id):
        report = get_object_or_404(EmergencyReport, id=report_id)

        # Ensure only responders can trigger crowdsourcing
        if request.user.profile.authority_level != 'Responder':
            return Response({
                'status': 'error',
                'message': 'Only responders can trigger crowdsourcing.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Identify nearby users (example logic, replace with actual distance calculation)
        nearby_users = UserProfile.objects.filter(
            status='approved',
            latitude__range=(report.latitude - 0.1, report.latitude + 0.1),
            longitude__range=(report.longitude - 0.1, report.longitude + 0.1)
        ).exclude(user=request.user)

        # Send verification prompts (mocked for now)
        for user in nearby_users:
            print(f"Sending verification request to {user.user.email}")

        return Response({
            'status': 'success',
            'message': 'Crowdsourcing verification triggered.',
            'notified_users': [user.user.email for user in nearby_users]
        }, status=status.HTTP_200_OK)

class RespondToEmergency(APIView):
    """
    API view for responders to mark a report as "Responded" and notify relevant users.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Mark an emergency report as responded and notify the reporter.",
        tags=['Emergency Reports'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['report_id'],
            properties={
                'report_id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='ID of the emergency report')
            }
        ),
        responses={
            200: "Report marked as responded",
            404: "Emergency report not found",
            401: "Authentication required"
        }
    )
    def post(self, request, report_id):
        report = get_object_or_404(EmergencyReport, id=report_id, responder=request.user)

        if report.status != 'Responding':
            return Response({
                'status': 'error',
                'message': 'Only reports in "Responding" status can be marked as "Responded."'
            }, status=status.HTTP_400_BAD_REQUEST)

        report.status = 'Responded'
        report.save()

        # Notify the reporter
        send_mail(
            subject='Responder En Route',
            message=f'A responder is en route to your reported emergency (ID: {report.id}).',
            from_email='noreply@alisto.com',
            recipient_list=[report.user.email]
        )

        return Response({
            'status': 'success',
            'message': 'The report has been marked as "Responded," and the reporter has been notified.'
        }, status=status.HTTP_200_OK)
