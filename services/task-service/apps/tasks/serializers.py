from rest_framework import serializers
from .models import Task, TaskRequirement


class TaskRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRequirement
        fields = ['id', 'input_data', 'expected_output', 'is_sample', 'created_at']
        read_only_fields = ['id', 'created_at']


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'tournament_id', 'title', 'difficulty', 'status', 'points', 'created_at']
        read_only_fields = ['id', 'created_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    requirements = TaskRequirementSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'tournament_id', 'title', 'description', 'difficulty',
            'status', 'time_limit', 'memory_limit', 'points',
            'requirements', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'tournament_id', 'title', 'description', 'difficulty',
            'status', 'time_limit', 'memory_limit', 'points'
        ]


class TaskStatisticsSerializer(serializers.Serializer):
    total_submissions = serializers.IntegerField()
    accepted_submissions = serializers.IntegerField()
    average_score = serializers.FloatField()
    success_rate = serializers.FloatField()
