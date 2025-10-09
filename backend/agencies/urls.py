from django.urls import path
from .views import (
    AgencyList, AgencyDetail,
    AgencyEmergencyTypeList, AgencyEmergencyTypeDetail
)

urlpatterns = [
    path('', AgencyList.as_view(), name='agency-list'),
    path('<uuid:pk>/', AgencyDetail.as_view(), name='agency-detail'),
    path('emergency-types/', AgencyEmergencyTypeList.as_view(), name='agency-emergency-type-list'),
    path('emergency-types/<uuid:pk>/', AgencyEmergencyTypeDetail.as_view(), name='agency-emergency-type-detail'),
]