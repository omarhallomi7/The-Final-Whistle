from django.shortcuts import render
from .forms import TeamForm
from pymongo import MongoClient
from footballApp.models import Match 
from django.db.models import Q


def home(request):
    return render(request, 'home.html')

def team_matches(request):
    matches = []
    team_name = None
    season = None

    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data["team_name"]
            season = form.cleaned_data["season"]
        matches = Match.objects.filter( (Q(HomeTeam__iexact=team_name) | Q(AwayTeam__iexact=team_name)) & Q(Season=season) )
    else:
        form = TeamForm()

    return render(request, "footballApp/team_matches.html", {
        "form": form,
        "matches": matches,
        "team_name": team_name,
        "season": season,
    })

