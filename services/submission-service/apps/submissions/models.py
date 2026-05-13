"""
Models для Task Service
OOP дизайн з методами, властивостями та бізнес-логікою
"""
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg


class Task(models.Model):
    """
    Модель завдання для турніру
    
    Атрибути:
    - tournament_id: ID турніру в tournament-service
    - created_by: ID користувача який створив завдання
    - title: назва завдання
    - description: детальний опис
    - tech_requirements: технічні вимоги (JSON)
    - start_time: коли можна почати розв'язувати
    - deadline: дедлайн подачи
    - status: (draft, published, closed)
    - created_at, updated_at: timestamps
    """
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    ]
    
    tournament_id = models.IntegerField(
        help_text="ID турніру з tournament-service"
    )
    created_by = models.IntegerField(
        help_text="ID користувача який створив"
    )
    title = models.CharField(
        max_length=255,
        help_text="Назва завдання"
    )
    description = models.TextField(
        help_text="Детальний опис завдання"
    )
    tech_requirements = models.JSONField(
        default=dict,
        blank=True,
        help_text="Технічні вимоги до проекту"
    )
    start_time = models.DateTimeField(
        help_text="Коли розпочнути розв'язування"
    )
    deadline = models.DateTimeField(
        help_text="Дедлайн для подачи"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['deadline']
        indexes = [
            models.Index(fields=['tournament_id', 'status']),
            models.Index(fields=['deadline']),
        ]
    
    def __str__(self):
        return f"[{self.tournament_id}] {self.title}"
    
    @property
    def is_active(self) -> bool:
        """Чи активне завдання (розпочалося але не скінчилось)"""
        now = timezone.now()
        return self.start_time <= now < self.deadline and self.status == 'published'
    
    @property
    def is_deadline_passed(self) -> bool:
        """Чи пройшов дедлайн"""
        return timezone.now() > self.deadline
    
    @property
    def time_remaining(self):
        """Скільки часу залишилось до дедлайну"""
        now = timezone.now()
        if now < self.deadline:
            return self.deadline - now
        return None
    
    def lock_all_submissions(self):
        """Заблокувати всі подачи (після дедлайну)"""
        self.submissions.filter(is_locked=False).update(
            is_locked=True,
            locked_at=timezone.now()
        )
    
    def get_statistics(self) -> dict:
        """Отримати статистику завдання"""
        submissions = self.submissions.all()
        return {
            'total_submissions': submissions.count(),
            'locked_submissions': submissions.filter(is_locked=True).count(),
            'requirements_count': self.requirements.count(),
            'avg_jury_score': self._get_avg_score(),
        }
    
    def _get_avg_score(self) -> float:
        """Розраховувати середню оцінку"""
        avg = self.submissions.values_list(
            'jury_assignments__scores__average_score',
            flat=True
        ).aggregate(Avg('jury_assignments__scores__average_score'))
        return avg.get('jury_assignments__scores__average_score__avg') or 0.0


class TaskRequirement(models.Model):
    """
    Модель вимоги завдання
    
    Атрибути:
    - task: FK на Task
    - title: назва вимоги
    - is_required: чи це обов'язкова вимога
    """
    
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='requirements',
        help_text="Завдання якому належить вимога"
    )
    title = models.CharField(
        max_length=255,
        help_text="Текст вимоги"
    )
    is_required = models.BooleanField(
        default=True,
        help_text="Чи обов'язкова вимога"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_required', 'created_at']
        unique_together = [['task', 'title']]
    
    def __str__(self):
        req_type = "Required" if self.is_required else "Optional"
        return f"{req_type}: {self.title}"


class Submission(models.Model):
    """
    Модель подачи розв'язку на завдання
    
    Атрибути:
    - task: FK на Task
    - team_id: ID команди (з tournament-service)
    - github_url: посилання на GitHub repo
    - video_url: посилання на відео презентації
    - live_demo_url: посилання на live demo
    - description: описання рішення
    - is_locked: чи заблокована від редагування
    - submitted_at, updated_at, locked_at: timestamps
    """
    
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='submissions',
        help_text="Завдання для якого подача"
    )
    team_id = models.IntegerField(
        help_text="ID команди з tournament-service"
    )
    github_url = models.URLField(
        blank=True,
        null=True,
        help_text="Посилання на GitHub репозиторій"
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text="Посилання на відео презентацію"
    )
    live_demo_url = models.URLField(
        blank=True,
        null=True,
        help_text="Посилання на live demo"
    )
    description = models.TextField(
        blank=True,
        help_text="Описання рішення та підходу"
    )
    is_locked = models.BooleanField(
        default=False,
        help_text="Чи заблокована від редагування"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    locked_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Коли була заблокована"
    )
    
    class Meta:
        ordering = ['-submitted_at']
        unique_together = [['task', 'team_id']]
        indexes = [
            models.Index(fields=['task', 'team_id']),
            models.Index(fields=['is_locked']),
        ]
    
    def __str__(self):
        return f"Team {self.team_id} submission for {self.task.title}"
    
    @property
    def can_edit(self) -> bool:
        """Чи можна редагувати подачу"""
        return not self.is_locked and not self.task.is_deadline_passed
    
    def lock(self):
        """Заблокувати подачу від редагування"""
        self.is_locked = True
        self.locked_at = timezone.now()
        self.save()
    
    def unlock(self):
        """Розблокувати подачу (admin only)"""
        self.is_locked = False
        self.locked_at = None
        self.save()
    
    def auto_lock_if_deadline_passed(self):
        """Автоматично заблокувати якщо дедлайн пройшов"""
        if self.task.is_deadline_passed and not self.is_locked:
            self.lock()
    
    def get_average_score(self) -> float:
        """Отримати середню оцінку від журі"""
        scores = self.jury_assignments.values_list(
            'scores__average_score',
            flat=True
        )
        if scores:
            return sum(scores) / len(scores)
        return 0.0


class JuryAssignment(models.Model):
    """
    Модель призначення журі для оцінювання подачи
    
    Атрибути:
    - submission: FK на Submission
    - jury_user_id: ID користувача журі (з user-service)
    - is_evaluated: чи оцінена подача
    - assigned_at: коли було призначено
    """
    
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='jury_assignments',
        help_text="Подача для оцінювання"
    )
    jury_user_id = models.IntegerField(
        help_text="ID користувача журі"
    )
    is_evaluated = models.BooleanField(
        default=False,
        help_text="Чи оцінена подача журі"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-assigned_at']
        unique_together = [['submission', 'jury_user_id']]
        indexes = [
            models.Index(fields=['jury_user_id', 'is_evaluated']),
        ]
    
    def __str__(self):
        status = "Evaluated" if self.is_evaluated else "Pending"
        return f"Jury {self.jury_user_id} - {status}"
    
    def mark_as_evaluated(self):
        """Позначити як оцінене"""
        self.is_evaluated = True
        self.save()
    
    def get_score_sum(self) -> float:
        """Отримати сумарну оцінку"""
        score = self.scores.first()
        return score.total_score if score else 0.0
    
    def get_has_score(self) -> bool:
        """Чи існує оцінка"""
        return self.scores.exists()


class Score(models.Model):
    """
    Модель оцінки подачи журі
    
    Атрибути:
    - assignment: FK на JuryAssignment
    - backend_code: оцінка за backend (0-100)
    - database: оцінка за БД (0-100)
    - frontend_code: оцінка за frontend (0-100)
    - functionality: оцінка за функціональність (0-100)
    - usability: оцінка за UX (0-100)
    - comment: коментар журі
    - evaluated_at: коли оцінено
    """
    
    assignment = models.ForeignKey(
        JuryAssignment,
        on_delete=models.CASCADE,
        related_name='scores',
        help_text="Призначення журі"
    )
    backend_code = models.IntegerField(
        default=0,
        help_text="Оцінка за backend код (0-100)"
    )
    database = models.IntegerField(
        default=0,
        help_text="Оцінка за архітектуру БД (0-100)"
    )
    frontend_code = models.IntegerField(
        default=0,
        help_text="Оцінка за frontend (0-100)"
    )
    functionality = models.IntegerField(
        default=0,
        help_text="Оцінка за функціональність (0-100)"
    )
    usability = models.IntegerField(
        default=0,
        help_text="Оцінка за UX/UI (0-100)"
    )
    comment = models.TextField(
        blank=True,
        help_text="Коментар журі"
    )
    evaluated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-evaluated_at']
        unique_together = [['assignment']]
    
    def __str__(self):
        return f"Score: {self.average_score:.1f}/100"
    
    @property
    def average_score(self) -> float:
        """Розраховувати середню оцінку"""
        scores = [
            self.backend_code,
            self.database,
            self.frontend_code,
            self.functionality,
            self.usability,
        ]
        return sum(scores) / len(scores) if scores else 0.0
    
    @property
    def total_score(self) -> int:
        """Сумарна оцінка (просто для зручності)"""
        return int(self.average_score)
    
    def clean(self):
        """Валідувати що всі оцінки в діапазоні 0-100"""
        from django.core.exceptions import ValidationError
        
        scores = {
            'backend_code': self.backend_code,
            'database': self.database,
            'frontend_code': self.frontend_code,
            'functionality': self.functionality,
            'usability': self.usability,
        }
        
        errors = {}
        for field, value in scores.items():
            if not (0 <= value <= 100):
                errors[field] = f"Score must be between 0 and 100, got {value}"
        
        if errors:
            raise ValidationError(errors)


class Leaderboard(models.Model):
    """
    Модель таблиці лідерів по турнірам
    
    Атрибути:
    - tournament_id: ID турніру
    - team_id: ID команди
    - total_score: сумарна оцінка команди
    - rank: місце в турнірі
    - calculated_at: коли був розраховуваний
    """
    
    tournament_id = models.IntegerField(
        help_text="ID турніру"
    )
    team_id = models.IntegerField(
        help_text="ID команди"
    )
    total_score = models.FloatField(
        default=0.0,
        help_text="Сумарна оцінка команди"
    )
    rank = models.IntegerField(
        default=0,
        help_text="Місце в турнірі"
    )
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['rank']
        unique_together = [['tournament_id', 'team_id']]
        indexes = [
            models.Index(fields=['tournament_id', 'rank']),
        ]
    
    def __str__(self):
        return f"#{self.rank} - Team {self.team_id} ({self.total_score:.2f})"
    
    @staticmethod
    def recalculate_tournament_leaderboard(tournament_id: int):
        """
        Пересчитати лідербордом для всього турніру
        
        Логіка:
        1. Для кожної команди в турнірі
        2. Отримати всі подачи команди
        3. Розрахувати середню оцінку всіх оцінок
        4. Оновити або створити запис в Leaderboard
        5. Встановити ranks на основі score
        """
        from django.db.models import Avg, F, Case, When, Value
        
        # Отримуємо всі команди які мають подачи для цього турніру
        teams_with_submissions = Submission.objects.filter(
            task__tournament_id=tournament_id
        ).values_list('team_id', flat=True).distinct()
        
        leaderboard_entries = []
        
        for team_id in teams_with_submissions:
            # Отримуємо усі оцінки для команди
            avg_score = Submission.objects.filter(
                task__tournament_id=tournament_id,
                team_id=team_id
            ).values_list(
                'jury_assignments__scores__average_score',
                flat=True
            ).aggregate(avg=Avg('jury_assignments__scores__average_score'))
            
            total_score = avg_score.get('avg') or 0.0
            
            # Оновлюємо або створюємо запис
            obj, created = Leaderboard.objects.update_or_create(
                tournament_id=tournament_id,
                team_id=team_id,
                defaults={'total_score': total_score}
            )
            leaderboard_entries.append(obj)
        
        # Встановлюємо ranks на основі score (найвищий = 1)
        sorted_entries = sorted(
            leaderboard_entries,
            key=lambda x: x.total_score,
            reverse=True
        )
        
        for rank, entry in enumerate(sorted_entries, 1):
            entry.rank = rank
            entry.save()
