from django import forms

class TeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name", max_length=100)
    season = forms.CharField(label="Season (e.g., 1999/2000)", max_length=9)

class HeadToHeadForm(forms.Form):
    team1 = forms.CharField(max_length=100, label="Team 1", widget=forms.TextInput(attrs={'placeholder': 'Enter Team 1'}))
    team2 = forms.CharField(max_length=100, label="Team 2", widget=forms.TextInput(attrs={'placeholder': 'Enter Team 2'}))
