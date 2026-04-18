from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status

from .models import Team
from .serializers import TeamListSerializer, TeamDetailSerializer, TeamRegisterSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404



class TeamRegisterView(APIView):

    def post(self, request):

        serializer = TeamRegisterSerializer(data=request.data)
        if serializer.is_valid():
            team = serializer.save()
            return Response({"detail": "Команда успішно зареєстрована", "team_id": team.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AdminTeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Team.objects.prefetch_related('members').all()

    @action(detail=False, url_path=r'tournaments/(?P<tournament_id>\d+)/teams', methods=['get'])
    def list_by_tournament(self, request, tournament_id=None):
        # Ми не перевіряємо Tournament через БД, бо її тут немає. 
        # В ідеалі — зробити запит до іншого мікросервісу для перевірки.
        teams = self.get_queryset().filter(tournament_id=tournament_id)
        
        page = self.paginate_queryset(teams)
        if page is not None:
            serializer = TeamListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TeamListSerializer(teams, many=True)
        return Response(serializer.data)