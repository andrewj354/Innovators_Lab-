from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Task, TaskRequirement
from .serializers import TaskRequirementSerializer

class TaskRequirementViewSet(viewsets.GenericViewSet):
    queryset = TaskRequirement.objects.all()
    serializer_class = TaskRequirementSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminUser()]

    # GET /api/tasks/{id}/requirements/
    @action(detail=False, methods=['get'], url_path=r'tasks/(?P<task_id>\d+)/requirements')
    def list_requirements(self, request, task_id=None):
        task = get_object_or_404(Task, pk=task_id)
        requirements = task.requirements.all()
        serializer = self.get_serializer(requirements, many=True)
        return Response(serializer.data)

    # POST /api/tasks/{id}/requirements/
    @action(detail=False, methods=['post'], url_path=r'tasks/(?P<task_id>\d+)/requirements')
    def add_requirement(self, request, task_id=None):
        task = get_object_or_404(Task, pk=task_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

from .serializers import TaskRequirementSerializer, AdminSubmissionSerializer

class TaskViewSet(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    
    def get_permissions(self):
        if self.action == 'submissions':
            return [IsAdminUser()] 
        return [IsAdminUser()]


    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser])
    def submissions(self, request, pk=None):
        """
        Повертає всі роботи (submissions) для конкретного завдання.
        Доступно тільки Admin/Jury.
        """
        task = self.get_object()
        submissions = task.submissions.all() 
        
        serializer = AdminSubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    @action(
        detail=True, 
        methods=['get'], 
        url_path='submissions',
        permission_classes=[permissions.IsAdminUser] 
    )
    def submissions(self, request, pk=None):
        """
        GET /api/tasks/{id}/submissions/
        Виводить всі роботи учасників для цього завдання.
        """
        task = self.get_object()
        
        task.update_status_by_time()
        
        submissions = task.submissions.all() 
        serializer = AdminSubmissionListSerializer(submissions, many=True)
        return Response(serializer.data)