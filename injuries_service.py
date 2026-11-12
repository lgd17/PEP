#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
injuries_service.py

Analyse des absents (blessés / suspendus)

Entrée :
    data/candidates.json

Sortie :
    data/injuries_analysis.json
"""

import json
from pathlib import Path

from api_utils import make_request

BASE_URL = "https://v2.football.sportsapipro.com"

INPUT_FILE = "data/candidates.json"
OUTPUT_FILE = "data/injuries_analysis.json"


def fetch_missing_players(match_id):

    response = make_request(
        "GET",
        f"{BASE_URL}/api/match/{match_id}/missing-players"
    )

    if response is None:
        return None

    try:
        return response.json()
    except Exception:
        return None


def calculate_injury_score(
    home_missing,
    away_missing
):
    """
    Plus l'adversaire a d'absents,
    plus le score est favorable.
    """

    delta = away_missing - home_missing

    score = 50 + (delta * 10)

    score = max(0, min(100, score))

    return round(score, 2)


def count_missing_players(data):

    if not data:
        return 0

    if isinstance(data, list):
        return len(data)

    if isinstance(data, dict):

        if "players" in data:
            return len(data["players"])

        if "missingPlayers" in data:
            return len(data["missingPlayers"])

        if "items" in data:
            return len(data["items"])

    return 0


def main():

    source = Path(INPUT_FILE)

    if not source.exists():

        print(
            f"❌ {INPUT_FILE} introuvable"
        )

        return

    payload = json.loads(
        source.read_text(
            encoding="utf-8"
        )
    )

    matches = payload.get(
        "matches",
        []
    )

    results = []

    for match in matches:

        match_id = match.get("id")

        if not match_id:
            continue

        home_team = (
            match.get("homeTeam", {})
            .get("name")
        )

        away_team = (
            match.get("awayTeam", {})
            .get("name")
        )

        print(
            f"🚑 Analyse absents : {home_team} vs {away_team}"
        )

        missing_data = fetch_missing_players(
            match_id
        )

        home_missing = 0
        away_missing = 0

        if missing_data:

            home_missing = count_missing_players(
                missing_data.get("home", [])
            )

            away_missing = count_missing_players(
                missing_data.get("away", [])
            )

        injury_score = calculate_injury_score(
            home_missing,
            away_missing
        )

        results.append({
            "match_id": match_id,

            "home_team": home_team,
            "away_team": away_team,

            "home_missing": home_missing,
            "away_missing": away_missing,

            "injuries_score": injury_score
        })

    output = {

        "analysis_type": "INJURIES",

        "count": len(results),

        "matches": results
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
        f"✅ Analyse blessures enregistrée : {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
      
