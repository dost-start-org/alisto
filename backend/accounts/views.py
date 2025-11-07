
# Django imports
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Rest framework imports
from rest_framework import generics, serializers, status, permissions, throttling
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView

# Third party imports
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView
from knox.auth import TokenAuthentication
from knox.models import AuthToken

# Local imports
from .models import User, UserProfile
from .permissions import IsLGUAdministrator
from .serializers import (
    RegisterSerializer, 
    UserSerializer, 
    PasswordResetRequestSerializer, 
    PasswordResetConfirmSerializer,
    EmailVerificationRequestSerializer, 
    EmailVerificationConfirmSerializer
)

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = 'register'

    @swagger_auto_schema(
        tags=['auth'],
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
        # Generate Knox token for the new user
        token = AuthToken.objects.create(user)[1]
        return Response({
            'ok': True,
            'email': user.email,
            'token': token,
        }, status=status.HTTP_201_CREATED)


class BaseLoginView(KnoxLoginView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = 'login'

    def _perform_login(self, request, user):
        """Log the user in when a session is available, otherwise emulate login side effects."""
        django_request = getattr(request, '_request', request)
        session = getattr(django_request, 'session', None)

        if session is not None:
            login(django_request, user)
            return

        # Emulate session-less login for token-based authentication flows
        user_logged_in.send(sender=user.__class__, request=django_request, user=user)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

    def get_user_profile_data(self, user):
        try:
            return {
                'id': str(user.id),  # Include user ID
                'full_name': user.profile.full_name,
                'authority_level': user.profile.authority_level,
                'contact_number': user.profile.contact_number,
                'address': user.profile.address,
                'status': user.profile.status,
                'email_verified': user.profile.email_verified,
                'latitude': str(user.profile.latitude) if user.profile.latitude else None,
                'longitude': str(user.profile.longitude) if user.profile.longitude else None,
                'emergency_contact_name': user.profile.emergency_contact_name,
                'emergency_contact_number': user.profile.emergency_contact_number,
            }
        except AttributeError:
            return None

    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'email and password required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({'error': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        self._perform_login(request, user)
        token = AuthToken.objects.create(user)[1]
        return Response({
            'ok': True,
            'email': user.email,
            'token': token,
            'profile': self.get_user_profile_data(user),
        })

class UserLoginAPIView(BaseLoginView):
    @swagger_auto_schema(
        tags=['auth'],
        operation_description="Login with email and password for normal users",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='User email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='User password'),
            }
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ok': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description='Knox authentication token'),
                        'profile': openapi.Schema(type=openapi.TYPE_OBJECT, description='User profile data')
                    }
                )
            ),
            400: "Invalid credentials",
            403: "Account not approved"
        }
    )

    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'email and password required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({'error': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if user.profile.authority_level != 'User':
                return Response({'error': 'Invalid user type for this endpoint'}, status=status.HTTP_403_FORBIDDEN)
            if user.profile.status != 'approved':
                return Response({'error': 'Account not approved. Please wait for LGU verification.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, format=format)

class ResponderLoginAPIView(BaseLoginView):
    @swagger_auto_schema(
        tags=['auth'],
        operation_description="Login with email and password for responder users",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Responder email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='Responder password'),
            }
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ok': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description='Knox authentication token'),
                        'profile': openapi.Schema(type=openapi.TYPE_OBJECT, description='Responder profile data')
                    }
                )
            ),
            400: "Invalid credentials",
            403: "Account not approved or not a responder"
        }
    )

    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'email and password required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({'error': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if user.profile.authority_level != 'Responder':
                return Response({'error': 'Invalid user type for this endpoint'}, status=status.HTTP_403_FORBIDDEN)
            if user.profile.status != 'approved':
                return Response({'error': 'Account not approved. Please wait for LGU verification.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, format=format)


# --- Password Reset Request ---
class PasswordResetRequestAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.AnonRateThrottle]
    throttle_scope = 'password_reset_request'

    @swagger_auto_schema(
        tags=['auth'],
        operation_description="Request a password reset email",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email address of the account to reset')
            }
        ),
        responses={
            200: openapi.Response(
                description="Password reset email sent (if account exists)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ok': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                    }
                )
            )
        }
    )

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

    @swagger_auto_schema(
        tags=['auth'],
        operation_description="Confirm password reset with token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['uid', 'token', 'password'],
            properties={
                'uid': openapi.Schema(type=openapi.TYPE_STRING, description='User ID from reset link'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='Reset token from email link'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='New password')
            }
        ),
        responses={
            200: openapi.Response(
                description="Password reset successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ok': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                    }
                )
            ),
            400: "Invalid or expired token"
        }
    )

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

    @swagger_auto_schema(
        tags=['auth'],
        operation_description="Request email verification link",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email address to verify')
            }
        ),
        responses={
            200: openapi.Response(
                description="Verification email sent (if account exists)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ok': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                    }
                )
            )
        }
    )

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

    @swagger_auto_schema(
        tags=['auth'],
        operation_description="Confirm email verification with token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['uid', 'token'],
            properties={
                'uid': openapi.Schema(type=openapi.TYPE_STRING, description='User ID from verification link'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='Verification token from email link')
            }
        ),
        responses={
            200: openapi.Response(
                description="Email verification successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ok': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                    }
                )
            ),
            400: "Invalid or expired token"
        }
    )

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


class LogoutAPIView(KnoxLogoutView):
    permission_classes = [IsAuthenticated]
    throttle_scope = 'login'
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        tags=['auth'],
        operation_description="Logout the current user and invalidate their token",
        responses={
            200: openapi.Response(
                description="Logout successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ok': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                    }
                )
            ),
            401: "Not authenticated"
        }
    )
    def post(self, request, format=None):
        knox_logout = super().post(request, format=None)
        return Response({'ok': True})


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        tags=['auth'],
        operation_description="Get current user information",
        responses={
            200: openapi.Response(
                description="Current user details",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            401: "Not authenticated"
        }
    )
    def get(self, request):
        user_data = UserSerializer(request.user).data
        profile_data = self.get_user_profile_data(request.user) if hasattr(request.user, 'profile') else None
        return Response({
            'user': user_data,
            'profile': profile_data,
            'email': request.user.email
        })
        
    def get_user_profile_data(self, user):
        try:
            return {
                'id': str(user.id),
                'full_name': user.profile.full_name,
                'authority_level': user.profile.authority_level,
                'contact_number': user.profile.contact_number,
                'address': user.profile.address,
                'status': user.profile.status,
                'email_verified': user.profile.email_verified,
                'latitude': str(user.profile.latitude) if user.profile.latitude else None,
                'longitude': str(user.profile.longitude) if user.profile.longitude else None,
                'emergency_contact_name': user.profile.emergency_contact_name,
                'emergency_contact_number': user.profile.emergency_contact_number,
            }
        except AttributeError:
            return None
