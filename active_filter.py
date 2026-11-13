#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
active_filter.py

Filtre qualité XPRONOS

Entrée :
    data/market_analysis.json

Sortie :
    data/active_matches.json
"""

import json
from pathlib import Path

INPUT_FILE = "data/market_analysis.json"

OUTPUT_FILE = "data/active_matches.json"

MIN_CONFIDENCE = 80


MARKET_ODDS_RULES = {

    "1": (1.40, 2.00),

    "2": (1.40, 2.00),

    "X": (2.50, 6.00),

    "BTTS_YES": (1.40, 4.00),

    "BTTS_NO": (1.40, 4.00),

    "OVER_1_5": (1.20, 2.00),

    "UNDER_1_5": (2.00, 6.00),

    "OVER_2_5": (1.50, 3.50),

    "UNDER_2_5": (1.50, 3.50),

    "OVER_3_5": (1.80, 6.00),

    "UNDER_3_5": (1.30, 3.50)
}


def load_data():

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


def odds_valid(
    market,
    odds
):

    if market not in MARKET_ODDS_RULES:
        return False

    minimum, maximum = (
        MARKET_ODDS_RULES[market]
    )

    return minimum <= odds <= maximum


def market_candidate(
    market,
    confidence,
    odds
):

    return (

        confidence >= MIN_CONFIDENCE

        and

        odds_valid(
            market,
            odds
        )
    )


def extract_markets(match):

    candidates = []

    odds_data = (
        match.get(
            "odds_payload",
            {}
        )
    )

    markets = match.get(
        "markets",
        {}
    )

    # 1X2

    one_x_two = markets.get(
        "1X2",
        {}
    )

    for key in (
        "1",
        "X",
        "2"
    ):

        confidence = one_x_two.get(
            key,
            0
        )

        odds = 1.80

        if market_candidate(
            key,
            confidence,
            odds
        ):

            candidates.append({

                "market": key,

                "confidence": confidence,

                "odds": odds
            })

    # BTTS

    btts = markets.get(
        "BTTS",
        {}
    )

    yes = btts.get(
        "YES",
        0
    )

    no = btts.get(
        "NO",
        0
    )

    if market_candidate(
        "BTTS_YES",
        yes,
        1.70
    ):
        candidates.append({

            "market": "BTTS_YES",

            "confidence": yes,

            "odds": 1.70
        })

    if market_candidate(
        "BTTS_NO",
        no,
        1.70
    ):
        candidates.append({

            "market": "BTTS_NO",

            "confidence": no,

            "odds": 1.70
        })

    totals = markets.get(
        "TOTALS",
        {}
    )

    for key in totals:

        confidence = totals[key]

        default_odds = {

            "OVER_1_5": 1.35,
            "UNDER_1_5": 4.30,

            "OVER_2_5": 1.80,
            "UNDER_2_5": 2.10,

            "OVER_3_5": 3.00,
            "UNDER_3_5": 1.50

        }.get(key, 1.80)

        if market_candidate(
            key,
            confidence,
            default_odds
        ):

            candidates.append({

                "market": key,

                "confidence":
                    confidence,

                "odds":
                    default_odds
            })

    return candidates


def build_active_match(match):

    candidates = extract_markets(
        match
    )

    candidates.sort(

        key=lambda x:

        x["confidence"],

        reverse=True
    )

    if not candidates:

        return None

    best_pick = candidates[0]

    second_pick = None

    if len(candidates) > 1:

        second_pick = candidates[1]

    exact_scores = match.get(
        "exact_scores",
        []
    )

    best_exact = None

    if exact_scores:

        best_exact = exact_scores[0]

    return {

        "match_id":
            match.get(
                "match_id"
            ),

        "home_team":
            match.get(
                "home_team"
            ),

        "away_team":
            match.get(
                "away_team"
            ),

        "score_xpronos":
            match.get(
                "score_xpronos"
            ),

        "active":
            True,

        "status":
            "ACTIF ✅",

        "best_pick":
            best_pick,

        "second_pick":
            second_pick,

        "best_exact_score":
            best_exact
    }


def main():

    matches = load_data()

    actives = []

    for match in matches:

        active_match = (
            build_active_match(
                match
            )
        )

        if active_match:

            actives.append(
                active_match
            )

    output = {

        "engine":
            "MRXPRONOS_V4",

        "min_confidence":
            MIN_CONFIDENCE,

        "count":
            len(actives),

        "matches":
            actives
    }

    Path(
        OUTPUT_FILE
    ).write_text(

        json.dumps(
            output,
            indent=2,
            ensure_ascii=False
        ),

        encoding="utf-8"
    )

    print(
        f"✅ {OUTPUT_FILE}"
    )

    print(
        f"🟢 Matchs actifs : {len(actives)}"
    )


if __name__ == "__main__":
    main()
