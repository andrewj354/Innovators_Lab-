"""
URL configuration для Task Service
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskViewSet, SubmissionViewSet, JuryAssignmentViewSet,
    ScoreViewSet, LeaderboardViewSet
)

# Ініціалізація router-а
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'submissions', SubmissionViewSet, basename='submission')
router.register(r'jury-assignments', JuryAssignmentViewSet, basename='jury-assignment')
router.register(r'scores', ScoreViewSet, basename='score')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')

urlpatterns = [
    path('', include(router.urls)),
]
