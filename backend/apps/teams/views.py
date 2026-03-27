from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.tournaments.models import Tournament
from .serializers import TeamRegisterSerializer

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