from django.urls import path
from .views import (
    EmergencyTypeList, EmergencyTypeDetail,
    EmergencyReportList, EmergencyReportDetail,
    EmergencyVerificationList, EmergencyVerificationDetail,
    UserEvaluationList, UserEvaluationDetail,
    TriggerCrowdsourcingBroadcast, MarkReportAsVerified
)

urlpatterns = [
    path('types/', EmergencyTypeList.as_view(), name='emergency-type-list'),
    path('types/<uuid:pk>/', EmergencyTypeDetail.as_view(), name='emergency-type-detail'),
    path('reports/', EmergencyReportList.as_view(), name='emergency-report-list'),
    path('reports/<uuid:pk>/', EmergencyReportDetail.as_view(), name='emergency-report-detail'),
    path('verifications/', EmergencyVerificationList.as_view(), name='emergency-verification-list'),
    path('verifications/<uuid:pk>/', EmergencyVerificationDetail.as_view(), name='emergency-verification-detail'),
    path('evaluations/', UserEvaluationList.as_view(), name='user-evaluation-list'),
    path('evaluations/<uuid:pk>/', UserEvaluationDetail.as_view(), name='user-evaluation-detail'),
    path('crowdsourcing/broadcast/', TriggerCrowdsourcingBroadcast.as_view(), name='trigger-crowdsourcing-broadcast'),
    path('crowdsourcing/mark-verified/', MarkReportAsVerified.as_view(), name='mark-report-as-verified'),
]
