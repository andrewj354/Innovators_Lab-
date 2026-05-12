"""
Views для Task Service
RESTful API endpoints для завдань, подач та оцінювання
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Avg, Count

from .models import Task, TaskRequirement, Submission, JuryAssignment, Score, Leaderboard
from .serializers import (
    TaskListSerializer, TaskDetailSerializer, TaskCreateUpdateSerializer,
    TaskRequirementSerializer,
    SubmissionListSerializer, SubmissionDetailSerializer, SubmissionCreateUpdateSerializer,
    JuryAssignmentListSerializer, JuryAssignmentDetailSerializer,
    ScoreSerializer,
    LeaderboardSerializer
)


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet для управління завданнями"""
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tournament_id', 'status']
    ordering_fields = ['deadline', 'created_at']
    ordering = ['deadline']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Вибір serializer-а на основі дії"""
        if self.action == 'retrieve':
            return TaskDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TaskCreateUpdateSerializer
        return TaskListSerializer
    
    def get_permissions(self):
        """Тільки admin може створювати завдання"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            from rest_framework.permissions import IsAdminUser
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """Встановити created_by на поточного користувача"""
        serializer.save(created_by=self.request.user.id)
    
    @action(detail=True, methods=['get'])
    def requirements(self, request, pk=None):
        """Отримати всі вимоги завдання"""
        task = self.get_object()
        requirements = task.requirements.all()
        serializer = TaskRequirementSerializer(requirements, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_requirement(self, request, pk=None):
        """Додати вимогу до завдання"""
        task = self.get_object()
        serializer = TaskRequirementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        """Отримати всі подачі для завдання"""
        task = self.get_object()
        submissions = task.submissions.all()
        serializer = SubmissionListSerializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Отримати статистику завдання"""
        task = self.get_object()
        submissions = task.submissions.all()
        
        return Response({
            'title': task.title,
            'tournament_id': task.tournament_id,
            'status': task.status,
            'is_active': task.is_active,
            'is_deadline_passed': task.is_deadline_passed,
            'deadline': task.deadline,
            'total_submissions': submissions.count(),
            'locked_submissions': submissions.filter(is_locked=True).count(),
            'requirements': task.requirements.count(),
            'must_have_requirements': task.requirements.filter(is_required=True).count(),
        })


class SubmissionViewSet(viewsets.ModelViewSet):
    """ViewSet для управління поданнями"""
    queryset = Submission.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['task', 'team_id', 'is_locked']
    ordering_fields = ['submitted_at']
    ordering = ['-submitted_at']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Вибір serializer-а на основі дії"""
        if self.action == 'retrieve':
            return SubmissionDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SubmissionCreateUpdateSerializer
        return SubmissionListSerializer
    
    def perform_create(self, serializer):
        """Створити подачу та auto-lock якщо дедлайн пройшов"""
        submission = serializer.save()
        submission.auto_lock_if_deadline_passed()
    
    @action(detail=True, methods=['post'])
    def lock(self, request, pk=None):
        """Заблокувати подачу від редагування"""
        submission = self.get_object()
        submission.lock()
        return Response({
            'status': 'success',
            'message': 'Submission locked',
            'is_locked': submission.is_locked
        })
    
    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None):
        """Розблокувати подачу (тільки для admin)"""
        submission = self.get_object()
        submission.unlock()
        return Response({
            'status': 'success',
            'message': 'Submission unlocked',
            'is_locked': submission.is_locked
        })
    
    @action(detail=True, methods=['get'])
    def jury_assignments(self, request, pk=None):
        """Отримати всі оцінки для подачі"""
        submission = self.get_object()
        assignments = submission.jury_assignments.all()
        serializer = JuryAssignmentListSerializer(assignments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Отримати подачи команди"""
        team_id = request.query_params.get('team_id')
        if not team_id:
            return Response(
                {'error': 'team_id parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submissions = self.queryset.filter(team_id=team_id)
        serializer = SubmissionListSerializer(submissions, many=True)
        return Response(serializer.data)


class JuryAssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet для управління призначеннями журі"""
    queryset = JuryAssignment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['submission', 'jury_user_id', 'is_evaluated']
    ordering_fields = ['assigned_at']
    ordering = ['-assigned_at']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Вибір serializer-а на основі дії"""
        if self.action == 'retrieve':
            return JuryAssignmentDetailSerializer
        return JuryAssignmentListSerializer
    
    @action(detail=False, methods=['get'])
    def my_assignments(self, request):
        """Отримати мої призначення для оцінювання"""
        jury_id = request.user.id
        assignments = self.queryset.filter(jury_user_id=jury_id)
        serializer = JuryAssignmentListSerializer(assignments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Отримати невиконані призначення"""
        jury_id = request.user.id
        assignments = self.queryset.filter(
            jury_user_id=jury_id,
            is_evaluated=False
        )
        serializer = JuryAssignmentListSerializer(assignments, many=True)
        return Response({
            'count': assignments.count(),
            'assignments': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def mark_as_evaluated(self, request, pk=None):
        """Позначити як оцінене"""
        assignment = self.get_object()
        assignment.mark_as_evaluated()
        return Response({
            'status': 'success',
            'message': 'Assignment marked as evaluated',
            'is_evaluated': assignment.is_evaluated
        })
    
    @action(detail=False, methods=['post'])
    def distribute_tasks(self, request):
        """
        Адмін action: випадково розподілити невиконані подачі між журі
        
        Параметри (JSON):
        - submission_ids: list[int] - список ID подач
        - jury_ids: list[int] - список ID журі
        - tasks_per_jury: int (optional, default=3) - кількість завдань на журі
        """
        import random
        
        # Тільки для admin
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin can distribute tasks'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        submission_ids = request.data.get('submission_ids', [])
        jury_ids = request.data.get('jury_ids', [])
        tasks_per_jury = request.data.get('tasks_per_jury', 3)
        
        if not submission_ids or not jury_ids:
            return Response(
                {'error': 'submission_ids and jury_ids required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Розподіляємо
        created_count = 0
        for submission_id in submission_ids:
            # Вибираємо random jury_ids для цієї подачи
            assigned_juries = random.sample(jury_ids, min(len(jury_ids), tasks_per_jury))
            
            submission = Submission.objects.filter(id=submission_id).first()
            if not submission:
                continue
            
            for jury_id in assigned_juries:
                # Уникаємо дублювання
                if not JuryAssignment.objects.filter(
                    submission=submission, jury_user_id=jury_id
                ).exists():
                    JuryAssignment.objects.create(
                        submission=submission,
                        jury_user_id=jury_id
                    )
                    created_count += 1
        
        return Response({
            'status': 'success',
            'created_assignments': created_count
        })


class ScoreViewSet(viewsets.ModelViewSet):
    """ViewSet для управління оцінками"""
    queryset = Score.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['assignment', 'assignment__submission__task']
    ordering_fields = ['evaluated_at']
    ordering = ['-evaluated_at']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        return ScoreSerializer
    
    def perform_create(self, serializer):
        """При створенні оцінки позначити assignment як evaluated"""
        score = serializer.save()
        score.assignment.mark_as_evaluated()
    
    def perform_update(self, serializer):
        """При оновленні оцінки"""
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def comparison(self, request, pk=None):
        """Порівняти оцінки для однієї подачи"""
        score = self.get_object()
        assignment = score.assignment
        submission = assignment.submission
        
        # Отримуємо всі оцінки для цієї подачи
        all_scores = Score.objects.filter(
            assignment__submission=submission
        )
        
        return Response({
            'submission_id': submission.id,
            'team_id': submission.team_id,
            'scores': ScoreSerializer(all_scores, many=True).data,
            'average': {
                'backend_code': all_scores.aggregate(Avg('backend_code'))['backend_code__avg'] or 0,
                'database': all_scores.aggregate(Avg('database'))['database__avg'] or 0,
                'frontend_code': all_scores.aggregate(Avg('frontend_code'))['frontend_code__avg'] or 0,
                'functionality': all_scores.aggregate(Avg('functionality'))['functionality__avg'] or 0,
                'usability': all_scores.aggregate(Avg('usability'))['usability__avg'] or 0,
            }
        })


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для таблиці лідерів (тільки читання)"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tournament_id']
    ordering = ['rank']
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_tournament(self, request):
        """Отримати лідербордом для турніру"""
        tournament_id = request.query_params.get('tournament_id')
        if not tournament_id:
            return Response(
                {'error': 'tournament_id parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leaderboard = self.queryset.filter(tournament_id=tournament_id)
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def recalculate(self, request):
        """Пересчитати лідербордом для турніру"""
        tournament_id = request.data.get('tournament_id')
        if not tournament_id:
            return Response(
                {'error': 'tournament_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        Leaderboard.recalculate_tournament_leaderboard(tournament_id)
        return Response({'status': 'success'})
    """ViewSet для управління поданнями"""
    queryset = Submission.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['task_id', 'team_id', 'is_locked']
    ordering_fields = ['submitted_at', 'updated_at']
    ordering = ['-submitted_at']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Вибір serializer-а на основі дії"""
        if self.action == 'retrieve':
            return SubmissionDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SubmissionCreateUpdateSerializer
        return SubmissionSerializer
    
    @action(detail=True, methods=['post'])
    def lock(self, request, pk=None):
        """Заблокувати подачу від редагування"""
        submission = self.get_object()
        submission.lock()
        return Response({
            'status': 'success',
            'message': 'Submission locked',
            'is_locked': submission.is_locked
        })
    
    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None):
        """Розблокувати подачу"""
        submission = self.get_object()
        submission.unlock()
        return Response({
            'status': 'success',
            'message': 'Submission unlocked',
            'is_locked': submission.is_locked
        })
    
    @action(detail=True, methods=['get'])
    def scores(self, request, pk=None):
        """Отримати всі оцінки подачі"""
        submission = self.get_object()
        assignments = submission.jury_assignments.all()
        
        scores_data = []
        for assignment in assignments:
            if assignment.scores.exists():
                score = assignment.scores.first()
                scores_data.append({
                    'jury_id': assignment.jury_user_id,
                    'scores': ScoreSerializer(score).data
                })
        
        return Response(scores_data)


class JuryAssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet для управління призначеннями журі"""
    queryset = JuryAssignment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['submission', 'jury_user_id', 'is_evaluated']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Вибір serializer-а на основі дії"""
        if self.action in ['create', 'update', 'partial_update']:
            return JuryAssignmentCreateSerializer
        return JuryAssignmentSerializer
    
    @action(detail=True, methods=['post'])
    def mark_as_evaluated(self, request, pk=None):
        """Позначити як оцінене"""
        assignment = self.get_object()
        assignment.mark_as_evaluated()
        return Response({
            'status': 'success',
            'message': 'Assignment marked as evaluated',
            'is_evaluated': assignment.is_evaluated
        })
    
    @action(detail=True, methods=['get'])
    def pending_assignments(self, request):
        """Отримати невиконані призначення для користувача"""
        jury_id = request.user.id
        pending = JuryAssignment.objects.filter(
            jury_user_id=jury_id,
            is_evaluated=False
        )
        serializer = JuryAssignmentSerializer(pending, many=True)
        return Response(serializer.data)


class ScoreViewSet(viewsets.ModelViewSet):
    """ViewSet для управління оцінками"""
    queryset = Score.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['assignment', 'assignment__submission']
    ordering_fields = ['evaluated_at']
    ordering = ['-evaluated_at']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Вибір serializer-а на основі дії"""
        if self.action in ['create', 'update', 'partial_update']:
            return ScoreCreateSerializer
        return ScoreSerializer
    
    def perform_create(self, serializer):
        """Створити оцінку та позначити як оцінене"""
        score = serializer.save()
        score.assignment.mark_as_evaluated()
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Отримати статистику оцінки"""
        score = self.get_object()
        return Response({
            'average_score': score.average_score,
            'total_score': score.total_score,
            'evaluated_at': score.evaluated_at,
            'jury_user_id': score.assignment.jury_user_id,
            'submission_id': score.assignment.submission_id
        })


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для таблиці лідерів (тільки читання)"""
    queryset = Leaderboard.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tournament_id']
    ordering_fields = ['rank']
    ordering = ['rank']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Вибір serializer-а на основі дії"""
        if self.action == 'list':
            return LeaderboardListSerializer
        elif self.action == 'retrieve':
            return LeaderboardDetailSerializer
        return LeaderboardSerializer
    
    @action(detail=False, methods=['get'])
    def by_tournament(self, request):
        """Отримати лідербордом для конкретного турніру"""
        tournament_id = request.query_params.get('tournament_id')
        
        if not tournament_id:
            return Response(
                {'error': 'tournament_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leaderboard = Leaderboard.objects.filter(
            tournament_id=tournament_id
        ).order_by('rank')
        
        serializer = LeaderboardListSerializer(leaderboard, many=True)
        return Response({
            'tournament_id': tournament_id,
            'leaderboard': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def recalculate(self, request):
        """Пересчитати лідербордом турніру"""
        tournament_id = request.data.get('tournament_id')
        
        if not tournament_id:
            return Response(
                {'error': 'tournament_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            Leaderboard.recalculate_tournament_leaderboard(tournament_id)
            return Response({
                'status': 'success',
                'message': f'Leaderboard for tournament {tournament_id} recalculated',
                'tournament_id': tournament_id
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def top_teams(self, request):
        """Отримати топ команди турніру"""
        tournament_id = request.query_params.get('tournament_id')
        limit = int(request.query_params.get('limit', 10))
        
        if not tournament_id:
            return Response(
                {'error': 'tournament_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        top = Leaderboard.objects.filter(
            tournament_id=tournament_id
        ).order_by('rank')[:limit]
        
        serializer = LeaderboardListSerializer(top, many=True)
        return Response({
            'tournament_id': tournament_id,
            'top_count': limit,
            'teams': serializer.data
        })
