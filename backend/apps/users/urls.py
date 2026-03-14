from django.urls import path
from .views import RegisterView, LoginView, Verify2FAView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('verify-2fa/', Verify2FAView.as_view(), name='verify-2fa'),
]