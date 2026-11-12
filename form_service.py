#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
form_service.py

Analyse de la forme récente des équipes.

Entrée :
    data/candidates.json

Sortie :
    data/form_analysis.json
"""

import json
from pathlib import Path

from api_utils import make_request

BASE_URL = "https://v2.football.sportsapipro.com"

INPUT_FILE = "data/candidates.json"
OUTPUT_FILE = "data/form_analysis.json"


def calculate_form_score(performance):

    """
    Convertit la forme récente en score sur 100.
    """

    if not performance:
        return 50

    wins = performance.get("wins", 0)
    draws = performance.get("draws", 0)
    losses = performance.get("losses", 0)

    total = wins + draws + losses

    if total == 0:
        return 50

    points = (
        wins * 3 +
        draws * 1
    )

    max_points = total * 3

    score = (
        points / max_points
    ) * 100

    return round(score, 2)


def fetch_team_performance(team_id):

    response = make_request(
        "GET",
        f"{BASE_URL}/api/teams/{team_id}/performance"
    )

    if response is None:
        return None

    try:
        return response.json()
    except Exception:
        return None


def main():

    path = Path(INPUT_FILE)

    if not path.exists():

        print(
            f"❌ {INPUT_FILE} introuvable"
        )

        return

    payload = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    matches = payload.get(
        "matches",
        []
    )

    results = []

    for match in matches:

        home_team = (
            match.get("homeTeam", {})
        )

        away_team = (
            match.get("awayTeam", {})
        )

        home_id = home_team.get("id")
        away_id = away_team.get("id")

        if not home_id or not away_id:
            continue

        print(
            f"📈 Forme : {home_team.get('name')} vs {away_team.get('name')}"
        )

        home_perf = fetch_team_performance(home_id)
        away_perf = fetch_team_performance(away_id)

        home_score = calculate_form_score(
            home_perf or {}
        )

        away_score = calculate_form_score(
            away_perf or {}
        )

        form_score = round(
            (
                home_score +
                (100 - away_score)
            ) / 2,
            2
        )

        results.append({

            "match_id": match.get("id"),

            "home_team":
                home_team.get("name"),

            "away_team":
                away_team.get("name"),

            "home_form_score":
                home_score,

            "away_form_score":
                away_score,

            "form_score":
                form_score
        })

    output = {

        "analysis_type":
            "FORM",

        "count":
            len(results),

        "matches":
            results
    }

    Path(
        OUTPUT_FILE
    ).write_text(

        json.dumps(
            output,
            ensure_ascii=False,
            indent=2
        ),

        encoding="utf-8"
    )

    print(
        f"✅ Analyse forme enregistrée dans {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
