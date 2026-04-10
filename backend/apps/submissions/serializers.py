from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            'id', 'task', 'team', 'github_url', 'video_url', 
            'live_demo_url', 'description', 'is_locked', 'submitted_at'
        ]
        read_only_fields = ['id', 'team', 'task', 'is_locked', 'submitted_at']

    def validate_github_url(self, value):
        if not value:
            raise serializers.ValidationError("GitHub URL є обов'язковим для подання роботи.")
        if "github.com" not in value.lower():
            raise serializers.ValidationError("Будь ласка, надайте валідне посилання на GitHub репозиторій.")
        return value