from django.urls import path
from .views import (
    EmergencyContactList, EmergencyContactDetail,
    ContactRedirectionList, ContactRedirectionDetail
)

urlpatterns = [
    path('contacts/', EmergencyContactList.as_view(), name='emergency-contact-list'),
    path('contacts/<uuid:pk>/', EmergencyContactDetail.as_view(), name='emergency-contact-detail'),
    path('redirections/', ContactRedirectionList.as_view(), name='contact-redirection-list'),
    path('redirections/<uuid:pk>/', ContactRedirectionDetail.as_view(), name='contact-redirection-detail'),
]