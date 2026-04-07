from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.shortcuts import get_object_or_404
from apps.tasks.models import Task, TaskStatus
from .models import Submission
from .serializers import SubmissionSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Submission.objects.filter(team__captain_email=user.email)

    @action(detail=False, methods=['post'], url_path=r'tasks/(?P<task_id>\d+)/submit')
    def submit_work(self, request, task_id=None):
        task = get_object_or_404(Task, pk=task_id)
        now = timezone.now()

        # 1. Валідація статусу та дедлайну
        if task.status == TaskStatus.SUBMISSION_CLOSED or now > task.deadline:
            return Response(
                {"error": "Час подання робіт вичерпано (дедлайн минув)."},
                status=status.HTTP_403_FORBIDDEN
            )
        from apps.teams.models import Team
        team = Team.objects.filter(captain_email=request.user.email).first()
        
        if not team:
            return Response({"error": "Ви не є капітаном жодної команди."}, status=status.HTTP_403_FORBIDDEN)

        # 3. Перевірка, чи вже було подання
        if Submission.objects.filter(task=task, team=team).exists():
            return Response({"error": "Робота вже була подана. Використовуйте PUT для редагування."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(team=team, task=task)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        submission = self.get_object()
        task = submission.task
        now = timezone.now()

        if submission.is_locked or now > task.deadline:
            submission.is_locked = True
            submission.save()
            return Response(
                {"error": "Редагування заблоковано: дедлайн минув або робота зафіксована."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)