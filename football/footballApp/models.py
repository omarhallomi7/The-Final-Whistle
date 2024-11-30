from djongo import models

class Match(models.Model):
    date = models.DateField()
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    fthg = models.IntegerField()  # Full-time home goals
    ftag = models.IntegerField()  # Full-time away goals
    ftr = models.CharField(max_length=1)  # Result: 'H', 'A', or 'D'
    winner = models.CharField(max_length=100)
    loser = models.CharField(max_length=100)
    season = models.CharField(max_length=9)  # Format: YYYY/YYYY

    class Meta:
        db_table = "PREMIER_LEAGUE"  # Match your MongoDB collection name
