from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('team-performance/', views.team_performance, name='team-performance'),
    path('world-cup/', views.world_cup, name='world_cup'),
    path('la-liga/', views.la_liga, name='la_liga'),
    path('premier-league/', views.premier_league, name='premier_league'),
    path('ligue-1/', views.ligue_1, name='ligue_1'),
    path('serie-a/', views.serie_a, name='serie_a'),
    path('h2h/', views.head_to_head_matches, name='h2h_form'),
]
