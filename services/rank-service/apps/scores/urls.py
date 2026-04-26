from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JuryScoringViewSet

router = DefaultRouter()
router.register(r'assignments', JuryScoringViewSet, basename='jury-assignments')

urlpatterns = [
    path('', include(router.urls)),
]