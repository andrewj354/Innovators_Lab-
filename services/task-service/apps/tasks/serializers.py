from rest_framework import serializers
from .models import TaskRequirement

class TaskRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRequirement
        fields = ['id', 'task', 'title', 'is_required']
        read_only_fields = ['task'] 