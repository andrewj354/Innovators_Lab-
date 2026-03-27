from django.db import models
from django.utils import timezone

class Tournament(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Registration', 'Registration'),
        ('Running', 'Running'),
        ('Finished', 'Finished'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    reg_start = models.DateTimeField()
    reg_end = models.DateTimeField()
    max_teams = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_status(self):
        now = timezone.now()

        if self.status == 'Draft' and now >= self.reg_start:
            self.status = 'Registration'
        elif self.status == 'Registration' and now >= self.reg_end:
            self.status = 'Running'
        elif self.status == 'Running' and now > self.reg_end:  
            self.status = 'Finished'

        self.save(update_fields=['status'])