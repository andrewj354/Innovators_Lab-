from django.urls import path
from .views import TournamentListCreateView, TournamentRetrieveUpdateDeleteView

urlpatterns = [
    path('', TournamentListCreateView.as_view(), name='tournament-list-create'),
    path('<int:pk>/', TournamentRetrieveUpdateDeleteView.as_view(), name='tournament-rud'),
]