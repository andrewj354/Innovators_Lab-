from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tournament
from .serializers import TournamentStatusSerializer

class TournamentStatusUpdateView(APIView):
    def patch(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({"detail": "Турнір не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TournamentStatusSerializer(tournament, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)