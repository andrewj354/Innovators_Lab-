from django.db import models

class Submission(models.Model):
    # Прямий зв'язок, бо Task у цьому ж сервісі
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='submissions')
    
    # Тільки ID, бо Team в іншому мікросервісі
    team_id = models.IntegerField(db_index=True)
    # Зберігаємо email для зручності фільтрації без запитів до іншого сервісу
    team_captain_email = models.EmailField(db_index=True)
    
    github_url = models.URLField()
    video_url = models.URLField(blank=True, null=True)
    live_demo_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    
    is_locked = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('task', 'team_id') # Одна команда — одна робота на один таск