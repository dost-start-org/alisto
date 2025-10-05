from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import EmergencyType, EmergencyReport, EmergencyVerification, UserEvaluation
from .serializers import (
    EmergencyTypeSerializer,
    EmergencyReportSerializer,
    EmergencyVerificationSerializer,
    UserEvaluationSerializer
)

class EmergencyTypeList(generics.ListCreateAPIView):
    queryset = EmergencyType.objects.all()
    serializer_class = EmergencyTypeSerializer

class EmergencyTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyType.objects.all()
    serializer_class = EmergencyTypeSerializer

class EmergencyReportList(generics.ListCreateAPIView):
    queryset = EmergencyReport.objects.all()
    serializer_class = EmergencyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EmergencyReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyReport.objects.all()
    serializer_class = EmergencyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmergencyVerificationList(generics.ListCreateAPIView):
    queryset = EmergencyVerification.objects.all()
    serializer_class = EmergencyVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EmergencyVerificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyVerification.objects.all()
    serializer_class = EmergencyVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserEvaluationList(generics.ListCreateAPIView):
    queryset = UserEvaluation.objects.all()
    serializer_class = UserEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserEvaluationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserEvaluation.objects.all()
    serializer_class = UserEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]
