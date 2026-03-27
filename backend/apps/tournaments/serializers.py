from rest_framework import serializers
from .models import Tournament
from apps.teams.models import Team  


# Serializer для створення турніру (Admin)
class TournamentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = [
            'title', 'description', 'reg_start', 'reg_end',
            'max_teams', 'status', 'created_by'
        ]
        read_only_fields = ['created_by']  



# Публічний список турнірів
class TournamentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = [
            'id', 'title', 'description', 'reg_start',
            'reg_end', 'status', 'max_teams'
        ]


# Деталі турніру + список команд
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'captain_email']  

class TournamentDetailSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True, source='team_set') 

    class Meta:
        model = Tournament
        fields = [
            'id', 'title', 'description', 'reg_start',
            'reg_end', 'status', 'max_teams', 'teams'
        ]



class TournamentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['status']

    def validate_status(self, value):
        current_status = self.instance.status
        order = ['Draft', 'Registration', 'Running', 'Finished']

        if order.index(value) < order.index(current_status):
            raise serializers.ValidationError("Неможливо змінити статус назад")
        return value