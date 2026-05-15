"""
URL configuration for task-service
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('tasks/', include('apps.tasks.urls')),
        path('submissions/', include('apps.submissions.urls')),
    ])),
]
