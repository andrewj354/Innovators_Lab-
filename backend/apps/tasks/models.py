from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class TaskStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    ACTIVE = 'active', 'Active'
    SUBMISSION_CLOSED = 'submission_closed', 'Submission Closed'
    EVALUATED = 'evaluated', 'Evaluated'

class Task(models.Model):
    # ... ваші попередні поля (title, start_time, deadline і т.д.) ...
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.DRAFT
    )

    # Порядок статусів для валідації "тільки вперед"
    STATUS_ORDER = {
        TaskStatus.DRAFT: 1,
        TaskStatus.ACTIVE: 2,
        TaskStatus.SUBMISSION_CLOSED: 3,
        TaskStatus.EVALUATED: 4,
    }

    def get_actual_status(self):
        """
        Метод для визначення статусу на основі часу.
        Якщо статус вже 'Evaluated', ми його не змінюємо автоматично.
        """
        if self.status == TaskStatus.EVALUATED:
            return TaskStatus.EVALUATED
            
        now = timezone.now()
        
        if now >= self.deadline:
            return TaskStatus.SUBMISSION_CLOSED
        if now >= self.start_time:
            return TaskStatus.ACTIVE
            
        return self.status

    def clean(self):
        """
        Валідація переходів статусу.
        """
        if self.pk:
            old_task = Task.objects.get(pk=self.pk)
            old_order = self.STATUS_ORDER.get(old_task.status, 0)
            new_order = self.STATUS_ORDER.get(self.status, 0)

            if new_order < old_order:
                raise ValidationError(
                    f"Не можна змінити статус з {old_task.status} назад на {self.status}."
                )

    def save(self, *args, **kwargs):
        # Оновлюємо статус перед збереженням, якщо він ще не фінальний
        if self.status != TaskStatus.EVALUATED:
            self.status = self.get_actual_status()
            
        self.full_clean() # Викликає clean() для перевірки логіки
        super().save(*args, **kwargs)