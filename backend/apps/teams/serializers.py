from rest_framework import serializers
from django.db import transaction
from .models import Team, TeamMember
from django.utils import timezone

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['full_name', 'email']

class TeamListSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(
        source='members.count', 
        read_only=True
    )
    tournament_name = serializers.CharField(
        source='tournament.title', 
        read_only=True
    )

    class Meta:
        model = Team
        fields = [
            'id', 
            'name', 
            'tournament_name', 
            'captain_name', 
            'captain_email', 
            'city', 
            'contact', 
            'members_count', 
            'registered_at'
        ]

class TeamRegisterSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True)

    class Meta:
        model = Team
        fields = ['name', 'captain_name', 'captain_email', 'city', 'contact', 'members']

    def validate_members(self, value):
        min_count = 2
        max_count = 10 
    
        if len(value) < min_count:
            raise serializers.ValidationError(f"Мінімальна кількість учасників: {min_count}")
        if len(value) > max_count:
            raise serializers.ValidationError(f"Максимальна кількість учасників: {max_count}")
            
        emails = [m['email'].lower() for m in value]
        if len(emails) != len(set(emails)):
            raise serializers.ValidationError("Email учасників у списку не повинні повторюватися")
            
        return value

    def validate(self, attrs):
        tournament = self.context.get('tournament')
        if not tournament:
            raise serializers.ValidationError("Турнір не знайдено в контексті")

        now = timezone.now()
        if not (tournament.reg_start <= now <= tournament.reg_end):
            raise serializers.ValidationError("Реєстрація на турнір закрита або ще не почалася")

        if Team.objects.filter(tournament=tournament, captain_email=attrs['captain_email']).exists():
            raise serializers.ValidationError("Команда з таким email капітана вже зареєстрована")

        if tournament.teams.count() >= tournament.max_teams:
            raise serializers.ValidationError("Ліміт команд для цього турніру вичерпано")

        return attrs

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        tournament = self.context['tournament']

        with transaction.atomic():
            team = Team.objects.create(tournament=tournament, **validated_data)
            
            member_instances = [
                TeamMember(team=team, **member_data)
                for member_data in members_data
            ]
            TeamMember.objects.bulk_create(member_instances)

        return team