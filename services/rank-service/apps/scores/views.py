from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import JuryAssignment, Score
from .serializers import ScoreCreateSerializer, ScoreDetailSerializer

class JuryScoringViewSet(viewsets.GenericViewSet):
    queryset = JuryAssignment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # POST /api/assignments/{id}/scores/
    @action(detail=True, methods=['post'], url_path='scores')
    def post_score(self, request, pk=None):
        assignment = self.get_object()
        user_id = request.user.id  # ID юзера з JWT токена

        # 1. Перевірка: Тільки призначений журі може оцінювати
        if assignment.jury_user_id != user_id:
            return Response(
                {"error": "Ви не призначені для оцінювання цієї роботи."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 2. Перевірка: Не можна оцінити двічі
        if hasattr(assignment, 'score'): # Якщо OneToOneField вже існує
            return Response(
                {"error": "Цю роботу вже оцінено. Використовуйте PUT для редагування."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ScoreCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Зберігаємо оцінку та оновлюємо статус призначення
        serializer.save(assignment=assignment)
        assignment.is_evaluated = True
        assignment.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # GET /api/assignments/{id}/scores/
    @action(detail=True, methods=['get'], url_path='scores')
    def get_score(self, request, pk=None):
        assignment = self.get_object()
        
        if not hasattr(assignment, 'score'):
            return Response(
                {"error": "Оцінка ще не виставлена."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ScoreDetailSerializer(assignment.score)
        return Response(serializer.data)