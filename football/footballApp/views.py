from django.shortcuts import render
from django.db.models import Q,Sum
from .forms import TeamForm,HeadToHeadForm
from .models import Match

def head_to_head_matches(request):
    matches = None
    team1_wins = 0
    team2_wins = 0
    draws = 0

    if request.method == 'POST':
        form = HeadToHeadForm(request.POST)
        if form.is_valid():
            team1 = form.cleaned_data['team1']
            team2 = form.cleaned_data['team2']

            # Query matches involving both teams
            matches = Match.objects.filter(
                (Q(HomeTeam=team1) & Q(AwayTeam=team2)) |
                (Q(HomeTeam=team2) & Q(AwayTeam=team1))
            ).order_by('-Date')

            # Calculate win/loss/draw counts
            for match in matches:
                if match.FTR == 'H' and match.HomeTeam == team1:
                    team1_wins += 1
                elif match.FTR == 'H' and match.HomeTeam == team2:
                    team2_wins += 1
                elif match.FTR == 'A' and match.AwayTeam == team1:
                    team1_wins += 1
                elif match.FTR == 'A' and match.AwayTeam == team2:
                    team2_wins += 1
                elif match.FTR == 'D':
                    draws += 1
    else:
        form = HeadToHeadForm()

    context = {
        'form': form,
        'matches': matches,
        'team1_wins': team1_wins,
        'team2_wins': team2_wins,
        'draws': draws,
    }
    return render(request, 'footballApp/h2h_matches_form.html', context)

def home(request):
    return render(request, 'home.html')

def world_cup(request):
    return render(request, 'footballApp/world_cup.html')

def la_liga(request):
    return render(request, 'footballApp/la_liga.html')

def premier_league(request):
    return render(request, 'footballApp/premier_league.html')

def ligue_1(request):
    return render(request, 'footballApp/ligue_1.html')

def serie_a(request):
    return render(request, 'footballApp/serie_a.html')

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