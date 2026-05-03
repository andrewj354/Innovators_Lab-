from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskRequirementViewSet, TaskViewSet
from .views import TaskAdminViewSet

router = DefaultRouter()
router.register(r'task-requirements', TaskRequirementViewSet, basename='task-requirements')

router.register(r'tasks', TaskAdminViewSet, basename='tasks')

urlpatterns = [
    path('tasks/<int:task_id>/requirements/', 
         TaskRequirementViewSet.as_view({'get': 'list_requirements', 'post': 'add_requirement'}), 
         name='task-requirements-api'),
    path('tasks/<int:pk>/submissions/', 
         TaskViewSet.as_view({'get': 'submissions'}), 
         name='task-submissions-list'),
    path('tournaments/<int:tournament_id>/tasks/', 
         TaskAdminViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='tournament-tasks'),
]