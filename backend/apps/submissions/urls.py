from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubmissionViewSet

router = DefaultRouter()
router.register(r'submissions', SubmissionViewSet, basename='submissions')

urlpatterns = [
    # POST /api/tasks/{id}/submit/
    path('tasks/<int:task_id>/submit/', 
         SubmissionViewSet.as_view({'post': 'submit_work'}), 
         name='task-submit'),
    
    path('', include(router.urls)),
]