from django.db import models
from django.conf import settings




class Tournament(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'Draft', 'Чорновик'
        REGISTRATION = 'Registration', 'Реєстрація'
        RUNNING = 'Running', 'Триває'
        FINISHED = 'Finished', 'Завершено'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    reg_start = models.DateTimeField()
    reg_end = models.DateTimeField()
    max_teams = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tournaments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"