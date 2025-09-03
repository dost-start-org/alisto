from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('login/', views.LoginAPIView.as_view(), name='api_login'),
    path('logout/', views.LogoutAPIView.as_view(), name='api_logout'),
    path('me/', views.MeAPIView.as_view(), name='api_me'),
]
