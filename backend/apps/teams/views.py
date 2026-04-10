from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from apps.tournaments.models import Tournament
from .models import Team
from .serializers import TeamListSerializer, TeamDetailSerializer, TeamRegisterSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class TeamRegisterView(APIView):

    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({"detail": "Турнір не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeamRegisterSerializer(data=request.data, context={'tournament': tournament})
        if serializer.is_valid():
            team = serializer.save()
            return Response({"detail": "Команда успішно зареєстрована", "team_id": team.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    







class AdminTeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamListSerializer
        if self.action in ['retrieve', 'update', 'partial_update']:
            return TeamDetailSerializer
        return TeamDetailSerializer

    def get_queryset(self):
        return Team.objects.select_related('tournament').prefetch_related('members').all()

    # GET /api/tournaments/{id}/teams/
    @action(detail=False, url_path=r'tournaments/(?P<tournament_id>\d+)/teams', methods=['get'])
    def list_by_tournament(self, request, tournament_id=None):
        tournament = get_object_or_404(Tournament, pk=tournament_id)
        teams = self.get_queryset().filter(tournament=tournament)
        
        page = self.paginate_queryset(teams)
        if page is not None:
            serializer = TeamListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TeamListSerializer(teams, many=True)
        return Response(serializer.data)