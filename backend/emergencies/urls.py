from django.urls import path
from .views import SendVerificationRequestView, VerificationResponseView, UpdateVerificationStatusView

urlpatterns = [
    path('send_verification_request/', SendVerificationRequestView.as_view(), name='send_verification_request'),
    path('verification_response/', VerificationResponseView.as_view(), name='verification_response'),
    path('update_verification_status/', UpdateVerificationStatusView.as_view(), name='update_verification_status'),
]
