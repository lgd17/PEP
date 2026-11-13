#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
odds_service.py

Analyse des cotes pré-match.

Entrée :
    data/candidates.json

Sortie :
    data/odds_analysis.json
"""

import json
from pathlib import Path

from api_utils import make_request

BASE_URL = "https://v2.football.sportsapipro.com"

INPUT_FILE = "data/candidates.json"
OUTPUT_FILE = "data/odds_analysis.json"


def load_candidates():

    path = Path(INPUT_FILE)

    if not path.exists():
        return []

    data = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    return data.get(
        "matches",
        []
    )


def fetch_odds(match_id):

    response = make_request(
        "GET",
        f"{BASE_URL}/api/match/{match_id}/odds/pre-match"
    )

    if response is None:
        return None

    try:
        return response.json()

    except Exception:
        return None


def extract_market(
    odds_payload,
    market_name
):

    markets = odds_payload.get(
        "markets",
        []
    )

    for market in markets:

        name = str(
            market.get("name", "")
        ).lower()

        if market_name.lower() in name:
            return market

    return None


def build_match_row(
    match,
    odds_payload
):

    return {

        "match_id":
            match.get("id"),

        "home_team":
            match.get(
                "homeTeam",
                {}
            ).get("name"),

        "away_team":
            match.get(
                "awayTeam",
                {}
            ).get("name"),

        "odds_payload":
            odds_payload
    }


def main():

    matches = load_candidates()

    results = []

    for match in matches:

        match_id = match.get("id")

        if not match_id:
            continue

        home = (
            match.get("homeTeam", {})
            .get("name")
        )

        away = (
            match.get("awayTeam", {})
            .get("name")
        )

        print(
            f"💰 Odds : {home} vs {away}"
        )

        odds = fetch_odds(
            match_id
        )

        if odds is None:

            continue

        results.append(
            build_match_row(
                match,
                odds
            )
        )

    output = {

        "analysis_type":
            "ODDS",

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
