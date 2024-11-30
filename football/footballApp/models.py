from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Match(models.Model):
    RESULT_CHOICES = [
        ('H', 'Home Win'),
        ('A', 'Away Win'),
        ('D', 'Draw'),
    ]

    date = models.DateField()
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    full_time_home_goals = models.IntegerField()
    full_time_away_goals = models.IntegerField()
    result = models.CharField(max_length=1, choices=RESULT_CHOICES)
    winner = models.ForeignKey(Team, related_name='wins', on_delete=models.CASCADE, null=True, blank=True)
    loser = models.ForeignKey(Team, related_name='losses', on_delete=models.CASCADE, null=True, blank=True)
    season = models.CharField(max_length=9)  # Format: 'YYYY/YYYY'

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.season})"
