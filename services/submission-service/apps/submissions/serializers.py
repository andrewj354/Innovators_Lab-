"""
Serializers для Task Service
Конвертують моделі в JSON та навпаки з валідацією
"""
from rest_framework import serializers
from django.utils import timezone
from .models import Task, TaskRequirement, Submission, JuryAssignment, Score, Leaderboard


# ============ TASK SERIALIZERS ============

class TaskRequirementSerializer(serializers.ModelSerializer):
    """Serializer для вимог завдання"""
    
    class Meta:
        model = TaskRequirement
        fields = ['id', 'title', 'is_required']
        read_only_fields = ['id']


class TaskListSerializer(serializers.ModelSerializer):
    """Serializer для списку завдань (мінімальна інформація)"""
    requirements_count = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'tournament_id', 'title', 'deadline', 'status', 
                  'is_active', 'time_remaining', 'requirements_count']
        read_only_fields = fields
    
    def get_requirements_count(self, obj):
        return obj.requirements.count()
    
    def get_is_active(self, obj):
        return obj.is_active
    
    def get_time_remaining(self, obj):
        tr = obj.time_remaining
        if tr:
            days = tr.days
            hours = tr.seconds // 3600
            return f"{days}d {hours}h"
        return "Deedline passed"


class TaskDetailSerializer(serializers.ModelSerializer):
    """Детальний serializer для завдання"""
    requirements = TaskRequirementSerializer(many=True, read_only=True)
    submissions_count = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'tournament_id', 'created_by', 'title', 'description',
                  'tech_requirements', 'start_time', 'deadline', 'status',
                  'is_active', 'time_remaining', 'requirements', 'submissions_count',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_submissions_count(self, obj):
        return obj.submissions.count()
    
    def get_is_active(self, obj):
        return obj.is_active
    
    def get_time_remaining(self, obj):
        tr = obj.time_remaining
        if tr:
            return tr.total_seconds()
        return 0


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer для створення/оновлення завдань"""
    requirements = TaskRequirementSerializer(many=True, required=False)
    
    class Meta:
        model = Task
        fields = ['tournament_id', 'title', 'description', 'tech_requirements',
                  'start_time', 'deadline', 'status', 'requirements']
    
    def validate(self, attrs):
        """Валідація часів"""
        start_time = attrs.get('start_time')
        deadline = attrs.get('deadline')
        
        if start_time and deadline:
            if start_time >= deadline:
                raise serializers.ValidationError(
                    "Start time must be before deadline"
                )
            if start_time < timezone.now():
                raise serializers.ValidationError(
                    "Start time must be in the future"
                )
        
        return attrs
    
    def create(self, validated_data):
        """Створити завдання та вимоги"""
        requirements_data = validated_data.pop('requirements', [])
        task = Task.objects.create(**validated_data)
        
        for req_data in requirements_data:
            TaskRequirement.objects.create(task=task, **req_data)
        
        return task
    
    def update(self, instance, validated_data):
        """Оновити завдання"""
        requirements_data = validated_data.pop('requirements', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if requirements_data is not None:
            instance.requirements.all().delete()
            for req_data in requirements_data:
                TaskRequirement.objects.create(task=instance, **req_data)
        
        return instance


# ============ SUBMISSION SERIALIZERS ============

class SubmissionListSerializer(serializers.ModelSerializer):
    """Serializer для списку подач"""
    can_edit = serializers.SerializerMethodField()
    task_title = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = ['id', 'task', 'task_title', 'team_id', 'is_locked', 
                  'can_edit', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']
    
    def get_can_edit(self, obj):
        return obj.can_edit
    
    def get_task_title(self, obj):
        return obj.task.title if obj.task else None


class SubmissionDetailSerializer(serializers.ModelSerializer):
    """Детальний serializer для подачі"""
    can_edit = serializers.SerializerMethodField()
    task_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = ['id', 'task', 'task_details', 'team_id', 'github_url',
                  'video_url', 'live_demo_url', 'description', 'is_locked',
                  'can_edit', 'submitted_at', 'updated_at']
        read_only_fields = ['id', 'is_locked', 'submitted_at', 'updated_at']
    
    def get_can_edit(self, obj):
        return obj.can_edit
    
    def get_task_details(self, obj):
        return {
            'id': obj.task.id,
            'title': obj.task.title,
            'deadline': obj.task.deadline,
            'is_active': obj.task.is_active,
            'is_deadline_passed': obj.task.is_deadline_passed
        }


class SubmissionCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer для створення/оновлення подач"""
    
    class Meta:
        model = Submission
        fields = ['task', 'team_id', 'github_url', 'video_url',
                  'live_demo_url', 'description']
    
    def validate(self, attrs):
        """Валідація подачі"""
        task = attrs.get('task')
        team_id = attrs.get('team_id')
        
        # Перевірити, чи дедлайн не пройшов
        if task and task.is_deadline_passed:
            raise serializers.ValidationError(
                "Cannot submit after deadline"
            )
        
        # Перевірити унікальність подачі
        if self.instance is None:  # На створення
            if Submission.objects.filter(task=task, team_id=team_id).exists():
                raise serializers.ValidationError(
                    "Team already submitted to this task"
                )
        
        return attrs


# ============ JURY SERIALIZERS ============

class ScoreSerializer(serializers.ModelSerializer):
    """Serializer для оцінок"""
    average_score = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()
    
    class Meta:
        model = Score
        fields = ['id', 'assignment', 'backend_code', 'database',
                  'frontend_code', 'functionality', 'usability', 'comment',
                  'average_score', 'total_score', 'evaluated_at']
        read_only_fields = ['id', 'evaluated_at', 'assignment']
    
    def get_average_score(self, obj):
        return round(obj.average_score, 2)
    
    def get_total_score(self, obj):
        return obj.total_score


class JuryAssignmentListSerializer(serializers.ModelSerializer):
    """Serializer для списку призначень журі"""
    submission_info = serializers.SerializerMethodField()
    score = ScoreSerializer(source='scores.first', read_only=True)
    
    class Meta:
        model = JuryAssignment
        fields = ['id', 'submission', 'submission_info', 'team_id',
                  'is_evaluated', 'score', 'assigned_at']
        read_only_fields = fields
    
    def get_submission_info(self, obj):
        sub = obj.submission
        return {
            'github_url': sub.github_url,
            'video_url': sub.video_url,
            'live_demo_url': sub.live_demo_url
        }
    
    def get_team_id(self, obj):
        return obj.submission.team_id


class JuryAssignmentDetailSerializer(serializers.ModelSerializer):
    """Детальний serializer для призначення журі"""
    submission_details = serializers.SerializerMethodField()
    scores = ScoreSerializer(many=True, read_only=True)
    
    class Meta:
        model = JuryAssignment
        fields = ['id', 'submission', 'submission_details', 'jury_user_id',
                  'is_evaluated', 'scores', 'assigned_at']
        read_only_fields = ['id', 'assigned_at', 'scores']
    
    def get_submission_details(self, obj):
        sub = obj.submission
        task = sub.task
        return {
            'team_id': sub.team_id,
            'task_title': task.title,
            'task_description': task.description,
            'github_url': sub.github_url,
            'video_url': sub.video_url,
            'live_demo_url': sub.live_demo_url,
            'requirements': [
                {'title': req.title, 'is_required': req.is_required}
                for req in task.requirements.all()
            ]
        }


# ============ LEADERBOARD SERIALIZERS ============

class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer для таблиці лідерів"""
    
    class Meta:
        model = Leaderboard
        fields = ['rank', 'team_id', 'total_score', 'calculated_at']
        read_only_fields = fields
    """Serializer для оцінок"""
    average_score = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()
    
    class Meta:
        model = Score
        fields = [
            'id', 'assignment', 'backend_code', 'database', 'frontend_code',
            'functionality', 'usability', 'comment', 'evaluated_at',
            'average_score', 'total_score'
        ]
        read_only_fields = ['id', 'evaluated_at']
    
    def get_average_score(self, obj):
        """Отримати середню оцінку"""
        return obj.average_score
    
    def get_total_score(self, obj):
        """Отримати загальну оцінку"""
        return obj.total_score


class ScoreCreateSerializer(serializers.ModelSerializer):
    """Serializer для створення оцінок"""
    
    class Meta:
        model = Score
        fields = [
            'assignment', 'backend_code', 'database', 'frontend_code',
            'functionality', 'usability', 'comment'
        ]
    
    def validate_scores(self, scores):
        """Валідація, що всі оцінки від 0 до 100"""
        if not all(0 <= score <= 100 for score in scores.values()):
            raise serializers.ValidationError(
                "All scores must be between 0 and 100"
            )
        return scores
    
    def validate(self, attrs):
        """Комплексна валідація"""
        score_fields = [
            'backend_code', 'database', 'frontend_code',
            'functionality', 'usability'
        ]
        scores = {field: attrs.get(field) for field in score_fields}
        
        return self.validate_scores(scores) or attrs


class JuryAssignmentSerializer(serializers.ModelSerializer):
    """Serializer для призначення журі"""
    score = ScoreSerializer(read_only=True)
    
    class Meta:
        model = JuryAssignment
        fields = [
            'id', 'submission', 'jury_user_id', 'is_evaluated',
            'assigned_at', 'score'
        ]
        read_only_fields = ['id', 'assigned_at']


class JuryAssignmentCreateSerializer(serializers.ModelSerializer):
    """Serializer для створення призначення журі"""
    
    class Meta:
        model = JuryAssignment
        fields = ['submission', 'jury_user_id']


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializer для подач"""
    jury_assignments = JuryAssignmentSerializer(many=True, read_only=True)
    can_edit = serializers.SerializerMethodField()
    has_all_urls = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = [
            'id', 'task_id', 'team_id', 'github_url', 'video_url',
            'live_demo_url', 'description', 'is_locked', 'submitted_at',
            'updated_at', 'jury_assignments', 'can_edit', 'has_all_urls'
        ]
        read_only_fields = ['id', 'submitted_at', 'updated_at']
    
    def get_can_edit(self, obj):
        """Перевірити, чи можна редагувати"""
        return obj.can_edit
    
    def get_has_all_urls(self, obj):
        """Перевірити, чи мають всі URL"""
        return obj.has_all_urls()


class SubmissionCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer для створення/оновлення подач"""
    
    class Meta:
        model = Submission
        fields = [
            'task_id', 'team_id', 'github_url', 'video_url',
            'live_demo_url', 'description'
        ]
    
    def validate_urls(self, urls):
        """Валідація URL форматів"""
        for url in urls:
            if url and not url.startswith(('http://', 'https://')):
                raise serializers.ValidationError(
                    "All URLs must start with http:// or https://"
                )
        return urls
    
    def validate(self, attrs):
        """Комплексна валідація"""
        urls = [
            attrs.get('github_url'),
            attrs.get('video_url'),
            attrs.get('live_demo_url')
        ]
        
        return self.validate_urls([u for u in urls if u]) or attrs


class SubmissionDetailSerializer(serializers.ModelSerializer):
    """Детальний serializer для подачі"""
    jury_assignments = JuryAssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Submission
        fields = [
            'id', 'task_id', 'team_id', 'github_url', 'video_url',
            'live_demo_url', 'description', 'is_locked', 'submitted_at',
            'updated_at', 'jury_assignments'
        ]
        read_only_fields = [
            'id', 'submitted_at', 'updated_at', 'jury_assignments'
        ]


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer для таблиці лідерів"""
    
    class Meta:
        model = Leaderboard
        fields = [
            'id', 'tournament_id', 'team_id', 'total_score', 'rank',
            'calculated_at'
        ]
        read_only_fields = [
            'id', 'total_score', 'rank', 'calculated_at'
        ]


class LeaderboardDetailSerializer(serializers.ModelSerializer):
    """Детальний serializer для лідербордом"""
    
    class Meta:
        model = Leaderboard
        fields = [
            'id', 'tournament_id', 'team_id', 'total_score', 'rank',
            'calculated_at'
        ]
        read_only_fields = [
            'id', 'total_score', 'rank', 'calculated_at'
        ]


class LeaderboardListSerializer(serializers.ModelSerializer):
    """Serializer для списку лідербордом"""
    
    class Meta:
        model = Leaderboard
        fields = [
            'team_id', 'total_score', 'rank'
        ]
        read_only_fields = fields
