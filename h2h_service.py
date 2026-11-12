#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
h2h_service.py

Analyse H2H (Head To Head)

Entrée :
    data/candidates.json

Sortie :
    data/h2h_analysis.json
"""

import json
from pathlib import Path

from api_utils import make_request

BASE_URL = "https://v2.football.sportsapipro.com"

INPUT_FILE = "data/candidates.json"
OUTPUT_FILE = "data/h2h_analysis.json"


def calculate_h2h_score(events):

    if not events:
        return 50

    home_wins = 0
    draws = 0
    away_wins = 0

    for event in events:

        try:

            home_score = event["homeScore"]["current"]
            away_score = event["awayScore"]["current"]

            if home_score > away_score:
                home_wins += 1

            elif home_score < away_score:
                away_wins += 1

            else:
                draws += 1

        except Exception:
            continue

    total = (
        home_wins +
        away_wins +
        draws
    )

    if total == 0:
        return 50

    score = (
        home_wins * 100
    ) / total

    return round(score, 2)


def fetch_h2h(match_id):

    response = make_request(
        "GET",
        f"{BASE_URL}/api/match/{match_id}/h2h"
    )

    if response is None:
        return None

    try:
        return response.json()
    except Exception:
        return None


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

        print(
            f"📊 H2H : {match_id}"
        )

        h2h_data = fetch_h2h(match_id)

        if not h2h_data:

            results.append({

                "match_id": match_id,

                "h2h_score": 50,

                "matches_found": 0
            })

            continue

        events = (
            h2h_data.get("events")
            or
            h2h_data.get("matches")
            or
            []
        )

        score = calculate_h2h_score(
            events
        )

        results.append({

            "match_id": match_id,

            "home_team":
                match.get("homeTeam", {})
                .get("name"),

            "away_team":
                match.get("awayTeam", {})
                .get("name"),

            "h2h_score":
                score,

            "matches_found":
                len(events)
        })

    output = {

        "analysis_type":
            "H2H",

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
        f"✅ H2H terminé : {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
