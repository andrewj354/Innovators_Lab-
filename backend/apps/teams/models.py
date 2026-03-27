from django.db import models
from apps.tournaments.models import Tournament

class Team(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=255)
    captain_name = models.CharField(max_length=255)
    captain_email = models.EmailField()
    city = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.tournament.title})"

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f"{self.full_name} ({self.team.name})"