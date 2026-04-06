from django.db import models
from django.conf import settings
from apps.tournaments.models import Tournament

class TaskStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    ACTIVE = 'active', 'Active'
    SUBMISSION_CLOSED = 'submission_closed', 'Submission Closed'
    EVALUATED = 'evaluated', 'Evaluated'

class Task(models.Model):
    tournament = models.ForeignKey(
        Tournament, 
        on_delete=models.CASCADE, 
        related_name='tasks',
        verbose_name="Турнір"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_tasks',
        verbose_name="Автор"
    )
    
    title = models.CharField(max_length=255, verbose_name="Назва завдання")
    description = models.TextField(verbose_name="Опис")
    tech_requirements = models.TextField(verbose_name="Технічні вимоги")
    
    start_time = models.DateTimeField(verbose_name="Час початку")
    deadline = models.DateTimeField(verbose_name="Дедлайн")
    
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.DRAFT,
        verbose_name="Статус"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Завдання"
        verbose_name_plural = "Завдання"
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"