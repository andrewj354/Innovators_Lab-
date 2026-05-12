"""
Views для Tournament Service
RESTful API endpoints
"""
from rest_framework import generics, status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import User, Tournament, Team, TeamMember, Task, TaskRequirement
from .serializers import (
    UserSerializer, UserCreateSerializer,
    TournamentSerializer, TournamentCreateUpdateSerializer, TournamentDetailSerializer,
    TeamSerializer, TeamCreateUpdateSerializer,
    TeamMemberSerializer,
    TaskSerializer, TaskCreateUpdateSerializer,
    TaskRequirementSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управління користувачами"""
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'email']
    filterset_fields = ['role']
    
    def get_serializer_class(self):
        """Вибір serializer-а на основі дії"""
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """Вибір дозволів на основі дії"""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]


class TournamentViewSet(viewsets.ModelViewSet):
    """ViewSet для управління турнірами"""
    queryset = Tournament.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'created_by']
    ordering_fields = ['created_at', 'reg_start']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Вибір serializer-а на основі дії"""
        if self.action == 'retrieve':
            return TournamentDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TournamentCreateUpdateSerializer
        return TournamentSerializer
    
    def perform_create(self, serializer):
        """Встановити created_by на поточного користувача"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def teams(self, request, pk=None):
        """Отримати всі команди турніру"""
        tournament = self.get_object()
        teams = tournament.teams.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        """Отримати всі завдання турніру"""
        tournament = self.get_object()
        tasks = tournament.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Отримати статистику турніру"""
        tournament = self.get_object()
        return Response({
            'teams_count': tournament.registered_teams_count,
            'max_teams': tournament.max_teams,
            'tasks_count': tournament.tasks.count(),
            'is_registration_open': tournament.is_registration_open,
            'can_accept_teams': tournament.can_accept_teams(),
            'status': tournament.status
        })


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet для управління командами"""
    queryset = Team.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tournament']
    search_fields = ['name', 'captain_name']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Вибір serializer-а на основі дії"""
        if self.action in ['create', 'update', 'partial_update']:
            return TeamCreateUpdateSerializer
        return TeamSerializer
    
    @action(detail=True, methods=['get', 'post'])
    def members(self, request, pk=None):
        """Отримати/додати членів команди"""
        team = self.get_object()
        
        if request.method == 'GET':
            members = team.members.all()
            serializer = TeamMemberSerializer(members, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = TeamMemberSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(team=team)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Отримати статистику команди"""
        team = self.get_object()
        return Response({
            'name': team.name,
            'captain': team.captain_name,
            'city': team.city,
            'members_count': team.members_count,
            'tournament_title': team.tournament.title,
            'registered_at': team.registered_at
        })


class TeamMemberViewSet(viewsets.ModelViewSet):
    """ViewSet для управління членами команди"""
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['team']
    search_fields = ['full_name', 'email']
    permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet для управління завданнями"""
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tournament', 'status']
    ordering_fields = ['start_time', 'deadline']
    ordering = ['start_time']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Вибір serializer-а на основі дії"""
        if self.action in ['create', 'update', 'partial_update']:
            return TaskCreateUpdateSerializer
        return TaskSerializer
    
    def perform_create(self, serializer):
        """Встановити created_by на поточного користувача"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get', 'post'])
    def requirements(self, request, pk=None):
        """Отримати/додати вимоги завдання"""
        task = self.get_object()
        
        if request.method == 'GET':
            requirements = task.requirements.all()
            serializer = TaskRequirementSerializer(requirements, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = TaskRequirementSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(task=task)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Отримати статистику завдання"""
        task = self.get_object()
        return Response({
            'title': task.title,
            'tournament': task.tournament.title,
            'is_active': task.is_active,
            'submissions_count': task.submissions_count,
            'requirements_count': task.requirements.count(),
            'deadline': task.deadline
        })


class TaskRequirementViewSet(viewsets.ModelViewSet):
    """ViewSet для управління вимогами завдань"""
    queryset = TaskRequirement.objects.all()
    serializer_class = TaskRequirementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task']
    permission_classes = [IsAuthenticated]
