from rest_framework import serializers
from .models import TaskRequirement
from apps.submission.models import Submission
from .models import Task, TaskStatus

class TaskSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'tournament_id', 'created_by', 'title', 'description', 
            'tech_requirements', 'start_time', 'deadline', 'status', 'status_display'
        ]
        read_only_fields = ['id', 'created_by']


class TaskRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRequirement
        fields = ['id', 'task', 'title', 'is_required']
        read_only_fields = ['task'] 

class AdminSubmissionSerializer(serializers.ModelSerializer):
    team = serializers.IntegerField(source='team_id') 
    status = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ['github_url', 'video_url', 'team', 'status', 'submitted_at']

    def get_status(self, obj):
        return "Submitted" if not obj.is_locked else "Locked"
    


class AdminSubmissionListSerializer(serializers.ModelSerializer):
    team = serializers.IntegerField(source='team_id')
    status = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ['github_url', 'video_url', 'team', 'status', 'submitted_at']

    def get_status(self, obj):
        # Можна додати складнішу логіку, якщо є оцінки
        return "Submitted" if not obj.is_locked else "Finalized"