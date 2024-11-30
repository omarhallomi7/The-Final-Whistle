from django import forms

class TeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name", max_length=100)
    season = forms.CharField(label="Season (e.g., 1999/2000)", max_length=9)
