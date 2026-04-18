from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            'id', 'task_id', 'team_id', 'github_url', 'video_url', 
            'live_demo_url', 'description', 'is_locked', 'submitted_at'
        ]
        read_only_fields = ['id', 'is_locked', 'submitted_at']