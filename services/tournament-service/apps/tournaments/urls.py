"""
URL configuration для Tournament Service
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, TournamentViewSet, TeamViewSet, TeamMemberViewSet,
    TaskViewSet, TaskRequirementViewSet
)

# Ініціалізація router-а
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tournaments', TournamentViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'team-members', TeamMemberViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'task-requirements', TaskRequirementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
