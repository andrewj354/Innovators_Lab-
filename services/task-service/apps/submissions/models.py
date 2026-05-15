from django.db import models
from django.utils.translation import gettext_lazy as _


class Submission(models.Model):
    """Team submission for a task - moved to submissions app"""
    
    class Status(models.TextChoices):
        SUBMITTED = 'submitted', _('Submitted')
        EVALUATING = 'evaluating', _('Evaluating')
        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')
        PARTIAL = 'partial', _('Partial')
    
    task_id = models.IntegerField()  # Reference to Task
    team_id = models.IntegerField()  # Reference to Team/User
    code = models.TextField()
    language = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED
    )
    passed_tests = models.IntegerField(default=0)
    total_tests = models.IntegerField(default=0)
    score = models.FloatField(default=0.0)
    
    is_locked = models.BooleanField(default=False)
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'submissions'
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['task_id']),
            models.Index(fields=['team_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Submission by team {self.team_id} for task {self.task_id}"
