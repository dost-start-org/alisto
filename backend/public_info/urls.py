from django.urls import path
from .views import (
    EmergencyContactList, EmergencyContactDetail,
    ContactRedirectionList, ContactRedirectionDetail,
    UserEmergencyContactListCreateView, UserEmergencyContactDetailView
)

urlpatterns = [
    path('contacts/', EmergencyContactList.as_view(), name='emergency-contact-list'),
    path('contacts/<uuid:pk>/', EmergencyContactDetail.as_view(), name='emergency-contact-detail'),
    path('redirections/', ContactRedirectionList.as_view(), name='contact-redirection-list'),
    path('redirections/<uuid:pk>/', ContactRedirectionDetail.as_view(), name='contact-redirection-detail'),
    path('user-contacts/', UserEmergencyContactListCreateView.as_view(), name='user-contact-list-create'),
    path('user-contacts/<uuid:pk>/', UserEmergencyContactDetailView.as_view(), name='user-contact-detail'),

]