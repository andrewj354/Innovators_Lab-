# apps/authentication/urls.py
from django.urls import path
from . import views
from apps.users.views import RegisterView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'healthy', 'service': 'user-service'})

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('refresh/', views.refresh_token, name='refresh'),
    path('me/', views.me_view, name='me'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('reset-password/', views.reset_password_view, name='reset-password'),
    path('2fa/enable/', views.enable_2fa_view, name='enable-2fa'),
    path('2fa/verify/', views.verify_2fa_view, name='verify-2fa'),
    path('2fa/verify-login/', views.verify_2fa_login_view, name='verify-2fa-login'),
    path('2fa/disable/', views.disable_2fa_view, name='disable-2fa'),
    path('health/', health_check),
]