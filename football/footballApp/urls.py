from django.urls import path
from .views import team_matches

urlpatterns = [
    path("team-matches/", team_matches, name="team_matches"),
]
