from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskRequirementViewSet

router = DefaultRouter()
router.register(r'task-requirements', TaskRequirementViewSet, basename='task-requirements')

urlpatterns = [
    path('tasks/<int:task_id>/requirements/', 
         TaskRequirementViewSet.as_view({'get': 'list_requirements', 'post': 'add_requirement'}), 
         name='task-requirements-api'),
]