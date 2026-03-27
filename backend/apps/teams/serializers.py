from rest_framework import serializers
from apps.tournaments.models import Tournament
from .models import Team, TeamMember
from django.utils import timezone

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['full_name', 'email']

class TeamRegisterSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True)

    class Meta:
        model = Team
        fields = ['name', 'captain_name', 'captain_email', 'city', 'contact', 'members']

    def validate(self, attrs):
        tournament = self.context['tournament']
        now = timezone.now()

        if not (tournament.reg_start <= now <= tournament.reg_end):
            raise serializers.ValidationError("Реєстрація на турнір закрита")

        if Team.objects.filter(tournament=tournament, captain_email=attrs['captain_email']).exists():
            raise serializers.ValidationError("Цей капітан вже зареєстрований на турнір")

        member_emails = [m['email'] for m in attrs['members']]
        if len(member_emails) != len(set(member_emails)):
            raise serializers.ValidationError("Email учасників не повинні повторюватися")

        return attrs

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        tournament = self.context['tournament']

        team = Team.objects.create(tournament=tournament, **validated_data)
        for member_data in members_data:
            TeamMember.objects.create(team=team, **member_data)

        return team