# apps/users/urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
]