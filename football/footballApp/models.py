from djongo import models

class Match(models.Model):
    Date = models.DateField()
    HomeTeam = models.CharField(max_length=100)
    AwayTeam = models.CharField(max_length=100)
    FTHG = models.IntegerField()  # Full-time home goals
    FTAG = models.IntegerField()  # Full-time away goals
    FTR = models.CharField(max_length=1)  # Result: 'H', 'A', or 'D'
    Winner = models.CharField(max_length=100)
    Loser = models.CharField(max_length=100)
    Season = models.CharField(max_length=9)  # Format: YYYY/YYYY

    class Meta:
        db_table = "PREMIER_LEAGUE"  # Match your MongoDB collection name
