from django.db import models
import uuid

class Team(models.Model):
    # Власний ID команди (автоматичний)
    id = models.AutoField(primary_key=True) 
    
    # ID турніру з іншого сервісу (просто число)
    tournament_id = models.IntegerField(verbose_name="ID Турніру", db_index=True)
    
    name = models.CharField(max_length=100, verbose_name="Назва команди")
    captain_name = models.CharField(max_length=100, verbose_name="Ім'я капітана")
    captain_email = models.EmailField(verbose_name="Email капітана")
    city = models.CharField(max_length=100, verbose_name="Місто")
    contact = models.CharField(max_length=100, verbose_name="Контактні дані")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата реєстрації")

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команди"
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.name} (Турнір ID: {self.tournament_id})"