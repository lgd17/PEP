#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
market_engine.py

Transforme le Score XPRONOS
en probabilités de marchés.

Entrée :
    data/detailed_analysis.json

Sortie :
    data/market_analysis.json
"""

import json
from pathlib import Path

INPUT_FILE = "data/detailed_analysis.json"
OUTPUT_FILE = "data/market_analysis.json"


def clamp(value, minimum=0, maximum=100):

    return max(
        minimum,
        min(
            maximum,
            round(value, 2)
        )
    )


def build_1x2(score):

    home = clamp(
        score
    )

    draw = clamp(
        100 - abs(
            score - 50
        ) * 2
    )

    away = clamp(
        100 - score
    )

    return {
        "1": home,
        "X": draw,
        "2": away
    }


def build_btts(score):

    yes = clamp(
        (score * 0.7) + 20
    )

    no = clamp(
        100 - yes
    )

    return {
        "YES": yes,
        "NO": no
    }


def build_totals(score):

    return {

        "OVER_1_5":
            clamp(
                score + 10
            ),

        "UNDER_1_5":
            clamp(
                100 - (score + 10)
            ),

        "OVER_2_5":
            clamp(
                score
            ),

        "UNDER_2_5":
            clamp(
                100 - score
            ),

        "OVER_3_5":
            clamp(
                score - 15
            ),

        "UNDER_3_5":
            clamp(
                100 - (score - 15)
            )
    }


def build_exact_scores(score):

    if score >= 90:

        return [

            {
                "score": "2-0",
                "confidence": 88
            },

            {
                "score": "2-1",
                "confidence": 85
            },

            {
                "score": "3-1",
                "confidence": 82
            }
        ]

    if score >= 80:

        return [

            {
                "score": "2-1",
                "confidence": 83
            },

            {
                "score": "1-0",
                "confidence": 80
            },

            {
                "score": "2-0",
                "confidence": 78
            }
        ]

    return [

        {
            "score": "1-1",
            "confidence": 70
        },

        {
            "score": "1-0",
            "confidence": 68
        },

        {
            "score": "0-0",
            "confidence": 65
        }
    ]


def load_matches():

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

    matches = load_matches()

    output_matches = []

    for match in matches:

        score = match.get(
            "score_xpronos",
            50
        )

        one_x_two = build_1x2(
            score
        )

        btts = build_btts(
            score
        )

        totals = build_totals(
            score
        )

        exact_scores = build_exact_scores(
            score
        )

        match["markets"] = {

            "1X2": one_x_two,

            "BTTS": btts,

            "TOTALS": totals
        }

        match["exact_scores"] = (
            exact_scores
        )

        output_matches.append(
            match
        )

    output = {

        "engine":
            "MRXPRONOS_V4",

        "count":
            len(output_matches),

        "matches":
            output_matches
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

    print(
        f"📊 Marchés générés : {len(output_matches)}"
    )


if __name__ == "__main__":
    main()
