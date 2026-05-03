from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class TaskStatus(models.TextChoices):
    DRAFT = 'draft', 'Чернетка'
    ACTIVE = 'active', 'Активне'
    SUBMISSION_CLOSED = 'submission_closed', 'Прийом закритий'
    EVALUATED = 'evaluated', 'Оцінено'

class Task(models.Model):

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

    def update_status_by_time(self):
        """Автоматичне оновлення статусу на основі часу без збереження в БД"""
        if self.status == TaskStatus.EVALUATED:
            return

        now = timezone.now()
        if now >= self.deadline:
            self.status = TaskStatus.SUBMISSION_CLOSED
        elif now >= self.start_time:
            if self.status == TaskStatus.DRAFT:
                self.status = TaskStatus.ACTIVE

    def clean(self):
        super().clean()
        if self.start_time and self.deadline and self.start_time >= self.deadline:
            raise ValidationError("Дата початку не може бути пізнішою за дедлайн.")

        if self.pk:

            original = Task.objects.get(pk=self.pk)
            old_order = self.STATUS_ORDER.get(original.status, 0)
            new_order = self.STATUS_ORDER.get(self.status, 0)

            if new_order < old_order:
                raise ValidationError(
                    f"Заборонено повертати статус назад з {original.get_status_display()} "
                    f"на {self.get_status_display()}."
                )

    def save(self, *args, **kwargs):

        self.update_status_by_time()
        self.full_clean()
        super().save(*args, **kwargs)