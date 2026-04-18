from rest_framework import serializers
from .models import Team,TeamMember



class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id','tournament_id','name','captain_name','captain_email','city','contact','registered_at']


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['full_name', 'email']


class TeamListSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(source='members.count', read_only=True)
    # Замість прямого доступу використовуємо SerializerMethodField
    tournament_name = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'tournament_id', 'tournament_name', 'captain_name', 'members_count', 'registered_at']

    def get_tournament_name(self, obj):
        return f"Турнір #{obj.tournament_id}"

class TeamDetailSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True, read_only=True)
    tournament_title = serializers.ReadOnlyField(source='tournament.title')

    class Meta:
        model = Team
        fields = '__all__' 