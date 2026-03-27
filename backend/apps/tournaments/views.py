from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tournament
from .serializers import TournamentStatusSerializer
from rest_framework import generics, filters
from .serializers import TournamentSerializer
from .permissions import IsAdminUser



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
    


class TournamentListCreateView(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['reg_start', 'reg_end', 'status']

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    permission_classes = [IsAdminUser]


class TournamentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminUser]