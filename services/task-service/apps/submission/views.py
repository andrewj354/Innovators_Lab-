from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .seializers import SubmissionSerializer
from .models import Submission
from apps.tasks.models import TaskStatus,Task


class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(team_captain_email=self.request.user.email)

    @action(detail=False, methods=['post'], url_path=r'tasks/(?P<task_id>\d+)/submit')
    def submit_work(self, request, task_id=None):
        task = get_object_or_404(Task, pk=task_id)
        
        if task.status == TaskStatus.SUBMISSION_CLOSEфD or timezone.now() > task.deadline:
            return Response(
                {"error": "Прийом робіт закритий (дедлайн минув)."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        team_id = request.data.get('team_id') 
        
        if Submission.objects.filter(task=task, team_id=team_id).exists():
            return Response(
                {"error": "Ви вже подали роботу. Оновіть існуючу через PATCH."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            task=task, 
            team_id=team_id, 
            team_captain_email=request.user.email
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        submission = self.get_object()
        if submission.task.status == TaskStatus.SUBMISSION_CLOSED or timezone.now() > submission.task.deadline:
            raise ValidationError("Неможливо редагувати: час вичерпано.")
        serializer.save()