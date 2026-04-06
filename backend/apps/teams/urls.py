from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminTeamViewSet

router = DefaultRouter()
router.register(r'teams', AdminTeamViewSet, basename='admin-teams')

urlpatterns = [

    path('tournaments/<int:tournament_id>/teams/', 
         AdminTeamViewSet.as_view({'get': 'list_by_tournament'}), 
         name='tournament-teams-list'),
    
    path('', include(router.urls)),
]