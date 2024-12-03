from django.shortcuts import render
from django.db.models import Q,Sum
from .forms import TeamForm
from .models import Match

def home(request):
    return render(request, 'home.html')

def team_performance(request):
    win_count = loss_count = draw_count = matches_played_count = None
    goals_scored = goals_conceded = None
    matches = None
    team_name = season = None

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data['team_name']
            season = form.cleaned_data['season']

            # Query matches played by the team in the specified season
            matches = Match.objects.filter(
                (Q(HomeTeam__iexact=team_name) | Q(AwayTeam__iexact=team_name)) & Q(Season=season)
            )

            # Count total matches played
            matches_played_count = matches.count()

            if matches_played_count > 0:
                # Goals scored as Home team
                home_goals_scored = matches.filter(HomeTeam__iexact=team_name).aggregate(total_home_goals=Sum('FTHG'))['total_home_goals'] or 0

                # Goals scored as Away team
                away_goals_scored = matches.filter(AwayTeam__iexact=team_name).aggregate(total_away_goals=Sum('FTAG'))['total_away_goals'] or 0

                # Total goals scored
                goals_scored = home_goals_scored + away_goals_scored

                # Goals conceded as Home team
                home_goals_conceded = matches.filter(HomeTeam__iexact=team_name).aggregate(total_home_conceded=Sum('FTAG'))['total_home_conceded'] or 0

                # Goals conceded as Away team
                away_goals_conceded = matches.filter(AwayTeam__iexact=team_name).aggregate(total_away_conceded=Sum('FTHG'))['total_away_conceded'] or 0

                # Total goals conceded
                goals_conceded = home_goals_conceded + away_goals_conceded

                # Count wins, losses, and draws
                # Wins: Home team won (FTR='H') or Away team won (FTR='A')
                home_wins = matches.filter(HomeTeam__iexact=team_name, FTR='H').count()
                away_wins = matches.filter(AwayTeam__iexact=team_name, FTR='A').count()
                win_count = home_wins + away_wins

                # Losses: Home team lost (FTR='A') or Away team lost (FTR='H')
                home_losses = matches.filter(HomeTeam__iexact=team_name, FTR='A').count()
                away_losses = matches.filter(AwayTeam__iexact=team_name, FTR='H').count()
                loss_count = home_losses + away_losses

                # Draws: Match ended in a draw (FTR='D')
                draw_count = matches.filter(Q(FTR='D') & (Q(HomeTeam__iexact=team_name) | Q(AwayTeam__iexact=team_name))).count()

    else:
        form = TeamForm()

    return render(request, 'footballApp/team_performance.html', {
        'form': form,
        'matches_played_count': matches_played_count,
        'win_count': win_count,
        'loss_count': loss_count,
        'draw_count': draw_count,
        'goals_scored': goals_scored,
        'goals_conceded': goals_conceded,
        'matches': matches,
        'team_name': team_name,
        'season': season,
    })