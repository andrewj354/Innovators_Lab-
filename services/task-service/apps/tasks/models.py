from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class TaskStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    ACTIVE = 'active', 'Active'
    SUBMISSION_CLOSED = 'submission_closed', 'Submission Closed'
    EVALUATED = 'evaluated', 'Evaluated'

class Task(models.Model):
    tournament_id = models.IntegerField(verbose_name="ID Турніру", db_index=True)
    created_by = models.IntegerField(verbose_name="Ким створений", db_index=True)
    
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Опис")
    tech_requirements = models.TextField(verbose_name="Технічні вимоги")
    
    start_time = models.DateTimeField(verbose_name="Час початку")
    deadline = models.DateTimeField(verbose_name="Дедлайн")
    
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.DRAFT,
        db_index=True
    )

    STATUS_ORDER = {
        TaskStatus.DRAFT: 1,
        TaskStatus.ACTIVE: 2,
        TaskStatus.SUBMISSION_CLOSED: 3,
        TaskStatus.EVALUATED: 4,
    }

    def clean(self):
        super().clean()
        
        if self.start_time and self.deadline:
            if self.start_time >= self.deadline:
                raise ValidationError("Дата початку не може бути пізнішою за дедлайн.")

        if self.pk:
            original = Task.objects.get(pk=self.pk)
            old_order = self.STATUS_ORDER.get(original.status, 0)
            new_order = self.STATUS_ORDER.get(self.status, 0)

            if new_order < old_order:
                raise ValidationError(
                    f"Не можна змінити статус назад з {original.get_status_display()} "
                    f"на {self.get_status_display()}."
                )

    def save(self, *args, **kwargs):

        if self.status != TaskStatus.EVALUATED:
            now = timezone.now()
            if now >= self.deadline:
                self.status = TaskStatus.SUBMISSION_CLOSED
            elif now >= self.start_time:
                if self.status == TaskStatus.DRAFT:
                    self.status = TaskStatus.ACTIVE
        
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Завдання"
        verbose_name_plural = "Завдання"