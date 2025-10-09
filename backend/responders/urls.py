from django.urls import path
from .views import ResponderList, ResponderDetail

urlpatterns = [
    path('', ResponderList.as_view(), name='responder-list'),
    path('<int:pk>/', ResponderDetail.as_view(), name='responder-detail'),
]