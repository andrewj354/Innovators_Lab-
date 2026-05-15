from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, Avg
from .models import Task, TaskRequirement
from .serializers import (
    TaskListSerializer,
    TaskDetailSerializer,
    TaskCreateUpdateSerializer,
    TaskRequirementSerializer,
    TaskStatisticsSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for Task management"""
    
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TaskCreateUpdateSerializer
        elif self.action == 'retrieve':
            return TaskDetailSerializer
        else:
            return TaskListSerializer
    
    def get_queryset(self):
        queryset = Task.objects.all()
        
        # Filter by tournament
        tournament_id = self.request.query_params.get('tournament_id')
        if tournament_id:
            queryset = queryset.filter(tournament_id=tournament_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Search by title
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def requirements(self, request, pk=None):
        """Get task requirements (test cases)"""
        task = self.get_object()
        requirements = task.requirements.all()
        serializer = TaskRequirementSerializer(requirements, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_requirement(self, request, pk=None):
        """Add new requirement to task"""
        task = self.get_object()
        serializer = TaskRequirementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get task statistics"""
        task = self.get_object()
        from apps.submissions.models import Submission
        
        submissions = Submission.objects.filter(task_id=task.id)
        total_submissions = submissions.count()
        accepted_submissions = submissions.filter(status='accepted').count()
        average_score = submissions.aggregate(avg=Avg('score'))['avg'] or 0
        success_rate = (accepted_submissions / total_submissions * 100) if total_submissions > 0 else 0
        
        data = {
            'total_submissions': total_submissions,
            'accepted_submissions': accepted_submissions,
            'average_score': average_score,
            'success_rate': success_rate
        }
        
        serializer = TaskStatisticsSerializer(data)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """Create new task (admin only)"""
        serializer.save()
    
    def perform_update(self, serializer):
        """Update task (admin only)"""
        serializer.save()


class HealthView(viewsets.ViewSet):
    """Health check endpoint"""
    
    @action(detail=False, methods=['get'])
    def health(self, request):
        return Response({'status': 'healthy'}, status=status.HTTP_200_OK)
