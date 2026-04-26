from rest_framework import serializers
from .models import Score, JuryAssignment

class ScoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = [
            'backend_code', 'database', 'frontend_code', 
            'functionality', 'usability', 'comment'
        ]

    def validate(self, data):

        fields_to_check = [
            'backend_code', 'database', 'frontend_code', 
            'functionality', 'usability'
        ]
        for field in fields_to_check:
            val = data.get(field)
            if val < 0 or val > 100:
                raise serializers.ValidationError({field: "Оцінка повинна бути в межах від 0 до 100."})
        return data
    

class ScoreDetailSerializer(serializers.ModelSerializer):
    average_score = serializers.ReadOnlyField() 

    class Meta:
        model = Score
        fields = [
            'id', 'backend_code', 'database', 'frontend_code', 
            'functionality', 'usability', 'comment', 'average_score', 'evaluated_at'
        ]


class JuryDashboardSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='submission.team.name', read_only=True)
    task_title = serializers.CharField(source='submission.task.title', read_only=True)
    github_url = serializers.URLField(source='submission.github_url', read_only=True)
    
    class Meta:
        model = JuryAssignment
        fields = [
            'id', 
            'team_name', 
            'task_title', 
            'github_url', 
            'is_evaluated', 
            'assigned_at'
        ]

class JuryAssignmentSerializer(serializers.ModelSerializer):
    submission_id = serializers.IntegerField(read_only=True) 
    is_evaluated = serializers.BooleanField(read_only=True)

    class Meta:
        model = JuryAssignment
        fields = ['id', 'submission_id', 'is_evaluated', 'assigned_at']