from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('team-matches/', views.team_matches, name='team-matches'),
]
