#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
standings_service.py

Analyse classement.

Entrée :
    data/candidates.json

Sortie :
    data/standings_analysis.json
"""

import json
from pathlib import Path

from api_utils import make_request

BASE_URL = "https://v2.football.sportsapipro.com"

INPUT_FILE = "data/candidates.json"
OUTPUT_FILE = "data/standings_analysis.json"


def compute_ranking_score(
    home_position,
    away_position
):

    if (
        home_position is None or
        away_position is None
    ):
        return 50

    delta = (
        away_position -
        home_position
    )

    score = 50 + (delta * 5)

    return max(
        0,
        min(100, score)
    )


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


def main():

    matches = load_candidates()

    results = []

    for match in matches:

        try:

            home_team = (
                match.get("homeTeam", {})
            )

            away_team = (
                match.get("awayTeam", {})
            )

            # À récupérer plus tard depuis standings
            home_position = (
                home_team.get(
                    "position"
                )
            )

            away_position = (
                away_team.get(
                    "position"
                )
            )

            ranking_score = (
                compute_ranking_score(
                    home_position,
                    away_position
                )
            )

            results.append({

                "match_id":
                    match.get("id"),

                "home_team":
                    home_team.get("name"),

                "away_team":
                    away_team.get("name"),

                "home_position":
                    home_position,

                "away_position":
                    away_position,

                "delta_position":
                    None
                    if home_position is None
                    else (
                        away_position -
                        home_position
                    ),

                "ranking_score":
                    ranking_score
            })

        except Exception:
            continue

    output = {

        "analysis_type":
            "STANDINGS",

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
