
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    # JWT Auth endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Password reset endpoints
    path('password-reset/request/', views.PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', views.PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),

    # Email verification endpoints
    path('email-verification/request/', views.EmailVerificationRequestAPIView.as_view(), name='email_verification_request'),
    path('email-verification/confirm/', views.EmailVerificationConfirmAPIView.as_view(), name='email_verification_confirm'),
]
