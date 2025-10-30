"""
URL configuration for nstw_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from emergencies.views import EmergencyReportResponderActions, EmergencyReportStatusUpdate, TriggerCrowdsourcing, RespondToEmergency

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint to verify system status
    """
    host = request.META.get('HTTP_HOST', '')
    print(f"Health check Host header: {host}")
    return JsonResponse({'status': 'healthy', 'host': host}, status=200)

schema_view = get_schema_view(
   openapi.Info(
      title="Alisto API",
      default_version='v1',
      description="API documentation for the Alisto emergency response system",
      terms_of_service="",
      contact=openapi.Contact(email="contact@alisto.example.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Health check endpoint
    path('health/', health_check, name='health_check'),
    
    path('admin/', admin.site.urls),
    # API routes
    path('api/auth/', include('accounts.urls')),
    path('api/emergencies/', include('emergencies.urls')),
    path('api/agencies/', include('agencies.urls')),
    path('api/public-info/', include('public_info.urls')),
    path('api/responders/', include('responders.urls')),
    
    # Swagger documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/emergencies/<uuid:report_id>/responder-actions/', EmergencyReportResponderActions.as_view(), name='emergency_report_responder_actions'),
    path('api/emergencies/<uuid:report_id>/status-update/', EmergencyReportStatusUpdate.as_view(), name='emergency_report_status_update'),
    path('api/emergencies/<uuid:report_id>/trigger-crowdsourcing/', TriggerCrowdsourcing.as_view(), name='trigger_crowdsourcing'),
    path('api/emergencies/<uuid:report_id>/respond/', RespondToEmergency.as_view(), name='respond_to_emergency'),
]
