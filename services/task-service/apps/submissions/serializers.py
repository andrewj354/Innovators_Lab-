from rest_framework import serializers
from .models import Submission


class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'task_id', 'team_id', 'language', 'status', 'score', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']


class SubmissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            'id', 'task_id', 'team_id', 'code', 'language', 'status',
            'passed_tests', 'total_tests', 'score', 'is_locked',
            'submitted_at', 'evaluated_at'
        ]
        read_only_fields = ['id', 'submitted_at', 'evaluated_at']


class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['task_id', 'code', 'language']


class SubmissionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['code', 'language', 'status']
