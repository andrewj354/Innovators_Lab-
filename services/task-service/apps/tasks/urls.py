from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, HealthView


router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'health', HealthView, basename='health')

urlpatterns = [
    path('', include(router.urls)),
]
