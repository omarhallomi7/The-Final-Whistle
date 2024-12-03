from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('team-performance/', views.team_performance, name='team-performance'),
]
