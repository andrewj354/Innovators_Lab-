"""
Serializers для Tournament Service
Конвертують моделі в JSON та навпаки з валідацією
"""
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import User, Tournament, Team, TeamMember, Task, TaskRequirement


class UserSerializer(serializers.ModelSerializer):
    """Базовий serializer для User"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer для реєстрації користувача"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'role', 'password', 'password_confirm']
    
    def validate_email(self, value):
        """Перевірка унікальності email"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value
    
    def validate(self, attrs):
        """Перевірка відповідності паролів"""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match'
            })
        return attrs
    
    def create(self, validated_data):
        """Створити користувача"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TaskRequirementSerializer(serializers.ModelSerializer):
    """Serializer для вимог завдання"""
    
    class Meta:
        model = TaskRequirement
        fields = ['id', 'title', 'is_required']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer для завдань"""
    requirements = TaskRequirementSerializer(many=True, read_only=True)
    submissions_count = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'tournament', 'created_by', 'title', 'description',
            'tech_requirements', 'start_time', 'deadline', 'status',
            'requirements', 'submissions_count', 'is_active'
        ]
        read_only_fields = ['id']
    
    def get_submissions_count(self, obj):
        """Отримати кількість подач"""
        return obj.submissions_count
    
    def get_is_active(self, obj):
        """Перевірити, чи завдання активне"""
        return obj.is_active


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer для створення/оновлення завдань"""
    
    class Meta:
        model = Task
        fields = [
            'tournament', 'title', 'description', 'tech_requirements',
            'start_time', 'deadline', 'status'
        ]
    
    def validate(self, attrs):
        """Валідація часів"""
        start_time = attrs.get('start_time')
        deadline = attrs.get('deadline')
        
        if start_time and deadline and start_time >= deadline:
            raise serializers.ValidationError(
                "Start time must be before deadline"
            )
        
        return attrs


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer для членів команди"""
    
    class Meta:
        model = TeamMember
        fields = ['id', 'full_name', 'email']
        read_only_fields = ['id']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer для команд"""
    members = TeamMemberSerializer(many=True, read_only=True)
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'tournament', 'name', 'captain_name', 'captain_email',
            'city', 'contact', 'registered_at', 'members', 'members_count'
        ]
        read_only_fields = ['id', 'registered_at']
    
    def get_members_count(self, obj):
        """Отримати кількість членів"""
        return obj.members_count


class TeamCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer для створення/оновлення команд"""
    
    class Meta:
        model = Team
        fields = [
            'tournament', 'name', 'captain_name', 'captain_email',
            'city', 'contact'
        ]


class TournamentSerializer(serializers.ModelSerializer):
    """Serializer для турнірів"""
    created_by = UserSerializer(read_only=True)
    teams = TeamSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    registered_teams_count = serializers.SerializerMethodField()
    is_registration_open = serializers.SerializerMethodField()
    can_accept_teams = serializers.SerializerMethodField()
    
    class Meta:
        model = Tournament
        fields = [
            'id', 'created_by', 'title', 'description', 'reg_start', 'reg_end',
            'max_teams', 'status', 'created_at', 'teams', 'tasks',
            'registered_teams_count', 'is_registration_open', 'can_accept_teams'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_registered_teams_count(self, obj):
        """Отримати кількість зареєстрованих команд"""
        return obj.registered_teams_count
    
    def get_is_registration_open(self, obj):
        """Перевірити, чи реєстрація відкрита"""
        return obj.is_registration_open
    
    def get_can_accept_teams(self, obj):
        """Перевірити, чи турнір може приймати команди"""
        return obj.can_accept_teams()


class TournamentCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer для створення/оновлення турнірів"""
    
    class Meta:
        model = Tournament
        fields = [
            'title', 'description', 'reg_start', 'reg_end',
            'max_teams', 'status'
        ]
    
    def validate(self, attrs):
        """Валідація часів реєстрації"""
        reg_start = attrs.get('reg_start')
        reg_end = attrs.get('reg_end')
        
        if reg_start and reg_end and reg_start >= reg_end:
            raise serializers.ValidationError(
                "Registration start must be before registration end"
            )
        
        # Перевірити, що дати в майбутньому
        if reg_start and reg_start < timezone.now():
            raise serializers.ValidationError(
                "Registration start must be in the future"
            )
        
        return attrs


class TournamentDetailSerializer(serializers.ModelSerializer):
    """Детальний serializer для турніру з усіма зв'язаними даними"""
    created_by = UserSerializer(read_only=True)
    teams = TeamSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Tournament
        fields = [
            'id', 'created_by', 'title', 'description', 'reg_start', 'reg_end',
            'max_teams', 'status', 'created_at', 'teams', 'tasks'
        ]
        read_only_fields = ['id', 'created_at']
