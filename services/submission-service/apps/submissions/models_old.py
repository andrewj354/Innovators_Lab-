from django.db import models
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import timedelta


class Task(models.Model):
    """
    Завдання/раунд для турніру
    
    Поля:
        - tournament_id: ID турніру (FK to tournament-service)
        - created_by: ID користувача, який створив (Admin)
        - title: Назва завдання
        - description: Описання завдання
        - tech_requirements: Технічні вимоги
        - start_time: Час початку завдання
        - deadline: Дедлайн для подачі
        - status: Статус (draft, published, closed)
    """
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Чернетка'
        PUBLISHED = 'published', 'Опубліковано'
        CLOSED = 'closed', 'Закрито'
    
    tournament_id = models.IntegerField()
    created_by = models.IntegerField()  # FK to user-service
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_requirements = models.TextField()
    start_time = models.DateTimeField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tasks'
        ordering = ['-deadline']
        indexes = [
            models.Index(fields=['tournament_id']),
            models.Index(fields=['status']),
            models.Index(fields=['deadline']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    @property
    def is_active(self) -> bool:
        """Чи завдання активне (в межах часу)"""
        now = timezone.now()
        return self.start_time <= now <= self.deadline
    
    @property
    def time_remaining(self):
        """Час до дедлайну"""
        diff = self.deadline - timezone.now()
        return diff if diff.total_seconds() > 0 else None
    
    @property
    def is_deadline_passed(self) -> bool:
        """Чи пройшов дедлайн"""
        return timezone.now() > self.deadline


class TaskRequirement(models.Model):
    """
    Вимога до завдання (must-have або optional)
    
    Поля:
        - task: FK до Task
        - title: Описання вимоги
        - is_required: Чи обов'язкова (True = must-have, False = nice-to-have)
    """
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='requirements')
    title = models.CharField(max_length=255)
    is_required = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'task_requirements'
        ordering = ['-is_required', 'title']
    
    def __str__(self):
        req_type = '🔴 Must-have' if self.is_required else '🟡 Nice-to-have'
        return f"{req_type}: {self.title}"


class Submission(models.Model):
    """
    Подача рішення команди на завдання
    
    Поля:
        - task: FK до Task
        - team_id: ID команди
        - github_url: URL GitHub репозиторію
        - video_url: URL відео демонстрації
        - live_demo_url: URL живої демонстрації
        - description: Описання подачі
        - is_locked: Чи заблокована від редагування (після дедлайну)
        - submitted_at: Дата подачі
        - updated_at: Дата оновлення
    """
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    team_id = models.IntegerField()  # FK to tournament-service Team
    github_url = models.URLField(validators=[URLValidator()], blank=True, null=True)
    video_url = models.URLField(validators=[URLValidator()], blank=True, null=True)
    live_demo_url = models.URLField(validators=[URLValidator()], blank=True, null=True)
    description = models.TextField(blank=True)
    is_locked = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'submissions'
        ordering = ['-submitted_at']
        unique_together = ('task', 'team_id')
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['team_id']),
            models.Index(fields=['is_locked']),
        ]
    
    def __str__(self):
        return f"Team#{self.team_id} → Task#{self.task_id}"
    
    @property
    def can_edit(self) -> bool:
        """Чи можна редагувати подачу"""
        return not self.is_locked and not self.task.is_deadline_passed
    
    def lock(self) -> None:
        """Заблокувати подачу від редагування"""
        self.is_locked = True
        self.save()
    
    def unlock(self) -> None:
        """Розблокувати подачу"""
        self.is_locked = False
        self.save()
    
    @property
    def score(self):
        """Отримати оцінку цієї подачи"""
        # Агрегація всіх оцінок від журі
        from django.db.models import Avg
        scores = self.jury_assignments.all().values('scores__average_score')
        if scores:
            avg = scores.aggregate(Avg('scores__average_score'))
            return avg.get('scores__average_score__avg', 0)
        return None


class JuryAssignment(models.Model):
    """
    Призначення подачі членам журі для оцінювання.
    
    Атрибути:
        id: Унікальний ідентифікатор
        submission_id: Подача для оцінювання
        jury_user_id: ID користувача-журі
        is_evaluated: Чи була подача оцінена цим журі
        assigned_at: Дата та час призначення
    """
    
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='jury_assignments')
    jury_user_id = models.IntegerField()  # FK to User service
    is_evaluated = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['assigned_at']
        db_table = 'jury_assignments'
        unique_together = ('submission', 'jury_user_id')
        indexes = [
            models.Index(fields=['submission']),
            models.Index(fields=['jury_user_id']),
        ]
    
    def __str__(self):
        return f"Jury#{self.jury_user_id} -> Submission#{self.submission_id}"
    
    def mark_as_evaluated(self) -> None:
        """Позначити як оцінене"""
        self.is_evaluated = True
        self.save()
    
    @property
    def score(self):
        """Отримати оцінку цього журі"""
        return self.scores.first() if self.scores.exists() else None


class Score(models.Model):
    """
    Оцінки подачі від журі.
    
    Атрибути:
        id: Унікальний ідентифікатор
        assignment_id: Призначення журі
        backend_code: Оцінка за код бекенду (0-100)
        database: Оцінка за роботу БД (0-100)
        frontend_code: Оцінка за код фронтенду (0-100)
        functionality: Оцінка за функціональність (0-100)
        usability: Оцінка за зручність використання (0-100)
        comment: Коментар журі
        evaluated_at: Дата та час оцінювання
    """
    
    assignment = models.ForeignKey(JuryAssignment, on_delete=models.CASCADE, related_name='scores')
    backend_code = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Оцінка за код бекенду (0-100)"
    )
    database = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Оцінка за БД (0-100)"
    )
    frontend_code = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Оцінка за код фронтенду (0-100)"
    )
    functionality = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Оцінка за функціональність (0-100)"
    )
    usability = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Оцінка за зручність (0-100)"
    )
    comment = models.TextField(blank=True)
    evaluated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-evaluated_at']
        db_table = 'scores'
        unique_together = ('assignment',)
    
    def __str__(self):
        return f"Score for Assignment#{self.assignment_id} (Avg: {self.average_score})"
    
    @property
    def average_score(self) -> float:
        """Обчислити середню оцінку"""
        scores = [
            self.backend_code,
            self.database,
            self.frontend_code,
            self.functionality,
            self.usability
        ]
        return sum(scores) / len(scores) if scores else 0.0
    
    @property
    def total_score(self) -> float:
        """Обчислити загальну оцінку (сума)"""
        return (
            self.backend_code +
            self.database +
            self.frontend_code +
            self.functionality +
            self.usability
        )


class Leaderboard(models.Model):
    """
    Таблиця лідерів турніру.
    
    Атрибути:
        id: Унікальний ідентифікатор
        tournament_id: ID турніру
        team_id: ID команди
        total_score: Загальна оцінка команди
        rank: Місце команди в рейтингу
        calculated_at: Дата та час останнього обчислення
    """
    
    tournament_id = models.IntegerField()  # FK to tournament-service Tournament
    team_id = models.IntegerField()  # FK to tournament-service Team
    total_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    rank = models.IntegerField(null=True, blank=True)
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['rank']
        db_table = 'leaderboard'
        unique_together = ('tournament_id', 'team_id')
        indexes = [
            models.Index(fields=['tournament_id']),
            models.Index(fields=['rank']),
        ]
    
    def __str__(self):
        return f"#{self.rank} Team#{self.team_id} ({self.total_score} pts)"
    
    def update_score(self, new_score: float) -> None:
        """Оновити оцінку команди"""
        self.total_score = new_score
        self.save()
    
    @staticmethod
    def recalculate_tournament_leaderboard(tournament_id: int) -> None:
        """
        Пересчитати лідерборд для турніру.
        Цей метод повинен бути викликаний після оцінювання.
        """
        # Отримуємо всі подачі для турніру
        from django.db.models import Avg
        
        # Оновлюємо оцінки кожної команди
        leaderboard_entries = Leaderboard.objects.filter(tournament_id=tournament_id)
        
        for entry in leaderboard_entries:
            # Обчислюємо середню оцінку для всіх подач команди
            avg_score = (
                Score.objects
                .filter(
                    assignment__submission__team_id=entry.team_id,
                    assignment__submission__task__tournament_id=tournament_id
                )
                .aggregate(Avg('backend_code'))['backend_code__avg'] or 0
            )
            entry.update_score(avg_score)
        
        # Оновлюємо рейтинги
        entries = leaderboard_entries.order_by('-total_score')
        for rank, entry in enumerate(entries, 1):
            entry.rank = rank
            entry.save()
