from django.shortcuts import render
from .forms import TeamForm
from pymongo import MongoClient

def team_matches(request):
    matches = []
    team_name = None
    season = None

    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data["team_name"]
            season = form.cleaned_data["season"]

            # Connect to MongoDB
            client = MongoClient("mongodb://localhost:27017/")  # Replace with your connection URI
            db = client["PREMIER_LEAGUE"]
            collection = db["PREMIER_LEAGUE"]

            # Query for matches where the team is either HomeTeam or AwayTeam in the specified season
            raw_matches = collection.find({
                "$and": [
                    {"Season": season},
                    {"$or": [
                        {"HomeTeam": {"$regex": f"^{team_name}$", "$options": "i"}},
                        {"AwayTeam": {"$regex": f"^{team_name}$", "$options": "i"}}
                    ]}
                ]
            })

            # Process matches to format goals and result
            matches = [
                {
                    **match,
                    "FTHG": int(match["FTHG"]),  # Convert Home Goals to integer
                    "FTAG": int(match["FTAG"]),  # Convert Away Goals to integer
                    "Result": f"{int(match['FTHG'])}-{int(match['FTAG'])}"  # Format Result
                }
                for match in raw_matches
            ]

            client.close()
    else:
        form = TeamForm()

    return render(request, "footballApp/team_matches.html", {
        "form": form,
        "matches": matches,
        "team_name": team_name,
        "season": season,
    })

