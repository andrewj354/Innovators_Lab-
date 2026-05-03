from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Score(models.Model):
    assignment = models.OneToOneField(
        'JuryAssignment', 
        on_delete=models.CASCADE, 
        related_name='score',
        verbose_name="Призначення журі"
    )
    
    # Оцінки за критеріями (діапазон 0-100)
    backend_code = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Backend Code"
    )
    database = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Database"
    )
    frontend_code = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Frontend Code"
    )
    functionality = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Functionality"
    )
    usability = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Usability"
    )
    
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар журі")
    evaluated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оцінювання")

    class Meta:
        verbose_name = "Оцінка"
        verbose_name_plural = "Оцінки"

    def __str__(self):
        return f"Score for Assignment #{self.assignment_id}"

    @property
    def average_score(self):
        """Розрахунок середнього балу для цієї оцінки"""
        scores = [
            self.backend_code, self.database, self.frontend_code, 
            self.functionality, self.usability
        ]
        return sum(scores) / len(scores)
    

from django.conf import settings

class JuryAssignment(models.Model):
    submission = models.ForeignKey(
        'Submission', 
        on_delete=models.CASCADE, 
        related_name='assignments',
        verbose_name="Робота"
    )

    jury_user_id = models.IntegerField(db_index=True, verbose_name="ID Судді")
    
    is_evaluated = models.BooleanField(default=False, verbose_name="Оцінено")
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата призначення")

    class Meta:
        verbose_name = "Призначення журі"
        verbose_name_plural = "Призначення журі"
        unique_together = ('submission', 'jury_user_id')

    def __str__(self):
        return f"Jury {self.jury_user_id} -> Submission {self.submission_id}"