#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
xg_service.py

Analyse xG
(expected goals)

Entrée :
    data/candidates.json

Sortie :
    data/xg_analysis.json
"""

import json
from pathlib import Path

from api_utils import make_request

BASE_URL = "https://v2.football.sportsapipro.com"

INPUT_FILE = "data/candidates.json"
OUTPUT_FILE = "data/xg_analysis.json"


def load_candidates():

    path = Path(INPUT_FILE)

    if not path.exists():
        return []

    payload = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    return payload.get(
        "matches",
        []
    )


def fetch_shotmap(match_id):

    response = make_request(
        "GET",
        f"{BASE_URL}/api/match/{match_id}/shotmap"
    )

    if response is None:
        return None

    try:
        return response.json()

    except Exception:
        return None


def calculate_xg_score(
    home_xg,
    away_xg
):

    total = home_xg + away_xg

    if total <= 0:
        return 50

    ratio = home_xg / total

    score = ratio * 100

    return round(
        score,
        2
    )


def extract_xg(data):

    if not data:
        return (
            0.0,
            0.0
        )

    home_xg = 0.0
    away_xg = 0.0

    shots = data.get(
        "shots",
        []
    )

    for shot in shots:

        try:

            xg = float(
                shot.get(
                    "xg",
                    0
                )
            )

            team = str(
                shot.get(
                    "team",
                    ""
                )
            ).lower()

            if "home" in team:
                home_xg += xg

            elif "away" in team:
                away_xg += xg

        except Exception:
            continue

    return (
        round(home_xg, 2),
        round(away_xg, 2)
    )


def main():

    matches = load_candidates()

    results = []

    for match in matches:

        match_id = match.get("id")

        if not match_id:
            continue

        home_team = (
            match.get(
                "homeTeam",
                {}
            ).get("name")
        )

        away_team = (
            match.get(
                "awayTeam",
                {}
            ).get("name")
        )

        print(
            f"📊 xG : {home_team} vs {away_team}"
        )

        shotmap = fetch_shotmap(
            match_id
        )

        home_xg = 0.0
        away_xg = 0.0

        if shotmap:

            (
                home_xg,
                away_xg
            ) = extract_xg(
                shotmap
            )

        xg_score = calculate_xg_score(
            home_xg,
            away_xg
        )

        results.append({

            "match_id":
                match_id,

            "home_team":
                home_team,

            "away_team":
                away_team,

            "home_xg":
                home_xg,

            "away_xg":
                away_xg,

            "xg_difference":
                round(
                    home_xg -
                    away_xg,
                    2
                ),

            "xg_score":
                xg_score
        })

    output = {

        "analysis_type":
            "XG",

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
        f"✅ {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
