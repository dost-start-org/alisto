
# --- Imports ---
from rest_framework import generics, serializers, status, permissions, throttling
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate, login, logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, UserProfile
from .serializers import RegisterSerializer, UserSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer, EmailVerificationRequestSerializer, EmailVerificationConfirmSerializer
from .permissions import IsLGUAdministrator

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = 'register'

    @swagger_auto_schema(
        operation_description="Register a new user account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password', 'first_name', 'last_name'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='User email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='User password'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User first name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User last name'),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING, description='User full name'),
                'authority_level': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description='User authority level',
                    enum=['Responder', 'User', 'LGU Administrator']
                ),
                'contact_number': openapi.Schema(type=openapi.TYPE_STRING, description='User contact number'),
                'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='User date of birth (YYYY-MM-DD)'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='User address'),
                'emergency_contact_name': openapi.Schema(type=openapi.TYPE_STRING, description='Emergency contact name'),
                'emergency_contact_number': openapi.Schema(type=openapi.TYPE_STRING, description='Emergency contact number')
            }
        ),
        responses={
            201: openapi.Response(
                description="User registered successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ok': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'access': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: "Invalid input or email already registered"
        },
    )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data['email']
        password = data['password']
        full_name = data.get('full_name')
        authority = data.get('authority_level')
        contact_number = data.get('contact_number')
        date_of_birth = data.get('date_of_birth')
        address = data.get('address')
        emergency_contact_name = data.get('emergency_contact_name')
        emergency_contact_number = data.get('emergency_contact_number')
        if User.objects.filter(email=email).exists():
            return Response({'error': 'email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            email=email, 
            password=password
        )
        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            authority_level=authority,
            contact_number=contact_number,
            date_of_birth=date_of_birth,
            address=address,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_number=emergency_contact_number,
            status='pending',
        )
        # Optionally send verification email here
        # Generate JWT token for the new user
        refresh = RefreshToken.for_user(user)
        return Response({
            'ok': True,
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = 'login'

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'email and password required'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({'error': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        # Check if user is approved
        try:
            if user.profile.status != 'approved':
                return Response({'error': 'Account not approved. Please wait for LGU verification.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'ok': True,
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


# --- Password Reset Request ---
class PasswordResetRequestAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.AnonRateThrottle]
    throttle_scope = 'password_reset_request'

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'ok': True})  # Don't reveal if user exists
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        send_mail(
            'Password Reset',
            f'Click the link to reset your password: {reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        return Response({'ok': True})


# --- Password Reset Confirm ---
class PasswordResetConfirmAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.AnonRateThrottle]
    throttle_scope = 'password_reset_confirm'

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({'ok': True})


# --- Email Verification Request ---
class EmailVerificationRequestAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.AnonRateThrottle]
    throttle_scope = 'email_verification_request'

    def post(self, request):
        serializer = EmailVerificationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'ok': True})
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verify_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"
        send_mail(
            'Verify your email',
            f'Click the link to verify your email: {verify_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        return Response({'ok': True})


# --- Email Verification Confirm ---
class EmailVerificationConfirmAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.AnonRateThrottle]
    throttle_scope = 'email_verification_confirm'

    def post(self, request):
        serializer = EmailVerificationConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        # Mark user as verified (add a field if needed)
        if hasattr(user, 'profile'):
            user.profile.email_verified = True
            user.profile.save()
        return Response({'ok': True})


class LogoutAPIView(APIView):
	# Require authenticated user for logout
	permission_classes = [IsAuthenticated]
	throttle_scope = 'login'

	def post(self, request):
		# Clear server-side session
		logout(request)
		return Response({'ok': True})


class MeAPIView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		return Response(UserSerializer(request.user).data)
