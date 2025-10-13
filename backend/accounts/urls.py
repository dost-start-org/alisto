
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('login/', views.UserLoginAPIView.as_view(), name='user_login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),  # Only keep the refresh endpoint

    # Password reset endpoints
    path('password-reset/request/', views.PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', views.PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),

    # Email verification endpoints
    path('email-verification/request/', views.EmailVerificationRequestAPIView.as_view(), name='email_verification_request'),
    path('email-verification/confirm/', views.EmailVerificationConfirmAPIView.as_view(), name='email_verification_confirm'),
]
