from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, Verify2FAView, MeView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('verify-2fa/', Verify2FAView.as_view()),
    path('me/', MeView.as_view()),

    # JWT refresh
    path('token/refresh/', TokenRefreshView.as_view()),
    path('google/', GoogleLoginView.as_view(), name='google-login'),
    path('google/callback/', GoogleCallbackView.as_view(), name='google-callback'),
]