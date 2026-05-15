from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    """Task/Problem for tournament"""
    
    class Difficulty(models.TextChoices):
        EASY = 'easy', _('Easy')
        MEDIUM = 'medium', _('Medium')
        HARD = 'hard', _('Hard')
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')
        ARCHIVED = 'archived', _('Archived')
    
    tournament_id = models.IntegerField()  # Reference to tournament-service
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    time_limit = models.IntegerField(help_text="Time limit in minutes", validators=[MinValueValidator(1)])
    memory_limit = models.IntegerField(help_text="Memory limit in MB", validators=[MinValueValidator(1)])
    points = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tasks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tournament_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"


class TaskRequirement(models.Model):
    """Requirements/Test cases for a task"""
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='requirements')
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False, help_text="Is this a sample test case?")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'task_requirements'
        ordering = ['id']
    
    def __str__(self):
        return f"Requirement for {self.task.title}"



