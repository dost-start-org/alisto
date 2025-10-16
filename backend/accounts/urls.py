
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('user/login/', views.UserLoginAPIView.as_view(), name='user_login'),
    path('user/responder/login/', views.ResponderLoginAPIView.as_view(), name='responder_login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),

    # Password reset endpoints
    path('password-reset/request/', views.PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', views.PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),

    # Email verification endpoints
    path('email-verification/request/', views.EmailVerificationRequestAPIView.as_view(), name='email_verification_request'),
    path('email-verification/confirm/', views.EmailVerificationConfirmAPIView.as_view(), name='email_verification_confirm'),
]
