from django.db import models
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    """
    Користувач системи з поддержкою ролей.
    
    Атрибути:
        name: Повне ім'я користувача
        email: Унікальна електронна пошта
        password_hash: Хеш пароля
        role: Роль користувача (admin, jury, team_lead, team_member)
        created_at: Дата та час реєстрації
    """
    
    class Role(models.TextChoices):
        """Ролі користувачів у системі"""
        ADMIN = 'admin', _('Адміністратор')
        JURY = 'jury', _('Журі')
        TEAM_LEAD = 'team_lead', _('Капітан команди')
        TEAM_MEMBER = 'team_member', _('Член команди')
    
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TEAM_MEMBER)
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'users'
    
    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"
    
    def is_admin(self) -> bool:
        """Перевірити, чи користувач є адміністратором"""
        return self.role == self.Role.ADMIN
    
    def is_jury(self) -> bool:
        """Перевірити, чи користувач є членом журі"""
        return self.role == self.Role.JURY
    
    def is_team_lead(self) -> bool:
        """Перевірити, чи користувач є капітаном команди"""
        return self.role == self.Role.TEAM_LEAD


class Tournament(models.Model):
    """
    Турнір/конкурс.
    
    Атрибути:
        id: Унікальний ідентифікатор
        created_by: Користувач, який створив турнір
        title: Назва турніру
        description: Опис турніру
        reg_start: Дата початку реєстрації команд
        reg_end: Дата закінчення реєстрації команд
        max_teams: Максимальна кількість команд
        status: Статус турніру (planning, registration, running, completed)
        created_at: Дата та час створення
    """
    
    class Status(models.TextChoices):
        """Статуси турніру"""
        PLANNING = 'planning', _('Планування')
        REGISTRATION = 'registration', _('Реєстрація')
        RUNNING = 'running', _('Проведення')
        COMPLETED = 'completed', _('Завершено')
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tournaments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    reg_start = models.DateTimeField()
    reg_end = models.DateTimeField()
    max_teams = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'tournaments'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_by']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    @property
    def is_registration_open(self) -> bool:
        """Перевірити, чи відкрита реєстрація"""
        now = datetime.now()
        return self.reg_start <= now <= self.reg_end
    
    @property
    def registered_teams_count(self) -> int:
        """Отримати кількість зареєстрованих команд"""
        return self.teams.count()
    
    def can_accept_teams(self) -> bool:
        """Перевірити, чи турнір може приймати нові команди"""
        return (self.is_registration_open and 
                self.registered_teams_count < self.max_teams and
                self.status == self.Status.REGISTRATION)


class Team(models.Model):
    """
    Команда, яка бере участь у турнірі.
    
    Атрибути:
        id: Унікальний ідентифікатор
        tournament_id: Турнір, до якого належить команда
        name: Назва команди
        captain_name: Ім'я капітана
        captain_email: Електронна пошта капітана
        city: Місто команди
        contact: Контактна інформація
        registered_at: Дата та час реєстрації
    """
    
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=255)
    captain_name = models.CharField(max_length=150)
    captain_email = models.EmailField()
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['registered_at']
        db_table = 'teams'
        unique_together = ('tournament', 'name')
        indexes = [
            models.Index(fields=['tournament']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.tournament.title})"
    
    @property
    def members_count(self) -> int:
        """Отримати кількість членів команди"""
        return self.members.count()


class TeamMember(models.Model):
    """
    Член команди.
    
    Атрибути:
        id: Унікальний ідентифікатор
        team_id: Команда, до якої належить член
        full_name: Повне ім'я члена
        email: Електронна пошта члена
    """
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    
    class Meta:
        ordering = ['full_name']
        db_table = 'team_members'
        unique_together = ('team', 'email')
    
    def __str__(self):
        return f"{self.full_name} ({self.team.name})"


class Task(models.Model):
    """
    Завдання для турніру.
    
    Атрибути:
        id: Унікальний ідентифікатор
        tournament_id: Турнір, до якого належить завдання
        created_by: Користувач, який створив завдання
        title: Назва завдання
        description: Опис завдання
        tech_requirements: Технічні вимоги
        start_time: Час початку завдання
        deadline: Дедлайн завдання
        status: Статус завдання (draft, published, closed)
    """
    
    class Status(models.TextChoices):
        """Статуси завдання"""
        DRAFT = 'draft', _('Чернетка')
        PUBLISHED = 'published', _('Опубліковано')
        CLOSED = 'closed', _('Закрито')
    
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_requirements = models.TextField()
    start_time = models.DateTimeField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    
    class Meta:
        ordering = ['start_time']
        db_table = 'tasks'
        indexes = [
            models.Index(fields=['tournament']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.tournament.title})"
    
    @property
    def is_active(self) -> bool:
        """Перевірити, чи завдання активне (в межах часу)"""
        now = datetime.now()
        return self.start_time <= now <= self.deadline
    
    @property
    def submissions_count(self) -> int:
        """Отримати кількість подач"""
        return self.submissions.count()


class TaskRequirement(models.Model):
    """
    Вимога для завдання.
    
    Атрибути:
        id: Унікальний ідентифікатор
        task_id: Завдання, до якого належить вимога
        title: Описання вимоги
        is_required: Чи є вимога обов'язковою
    """
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='requirements')
    title = models.CharField(max_length=255)
    is_required = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['task']
        db_table = 'task_requirements'
    
    def __str__(self):
        req_type = "Обов'язкова" if self.is_required else "Опціональна"
        return f"{self.title} ({req_type})"
