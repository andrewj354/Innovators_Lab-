from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Submission
from .serializers import (
    SubmissionListSerializer,
    SubmissionDetailSerializer,
    SubmissionCreateSerializer,
    SubmissionUpdateSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class SubmissionViewSet(viewsets.ModelViewSet):
    """ViewSet for Submission management"""
    
    queryset = Submission.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            if self.action == 'create':
                return SubmissionCreateSerializer
            else:
                return SubmissionUpdateSerializer
        elif self.action == 'retrieve':
            return SubmissionDetailSerializer
        else:
            return SubmissionListSerializer
    
    def get_queryset(self):
        queryset = Submission.objects.all()
        
        # Filter by task
        task_id = self.request.query_params.get('task_id')
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        
        # Filter by team
        team_id = self.request.query_params.get('team_id')
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get submissions by team"""
        team_id = request.query_params.get('team_id')
        if not team_id:
            return Response(
                {'error': 'team_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submissions = Submission.objects.filter(team_id=team_id)
        page = self.paginate_queryset(submissions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def lock(self, request, pk=None):
        """Lock a submission"""
        submission = self.get_object()
        submission.is_locked = True
        submission.save()
        serializer = self.get_serializer(submission)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None):
        """Unlock a submission"""
        submission = self.get_object()
        submission.is_locked = False
        submission.save()
        serializer = self.get_serializer(submission)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """Create new submission"""
        serializer.save()
    
    def perform_update(self, serializer):
        """Update submission"""
        serializer.save()
