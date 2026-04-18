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