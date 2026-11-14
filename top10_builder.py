#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
top10_builder.py

Construit le Top 10 final.

Entrée :
    data/active_matches.json

Sortie :
    data/top10_active.json
"""

import json
from pathlib import Path
from datetime import datetime


INPUT_FILE = "data/active_matches.json"
OUTPUT_FILE = "data/top10_active.json"

MAX_MATCHES = 10


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


def rank_matches(matches):

    return sorted(
        matches,
        key=lambda x: (
            x.get(
                "score_xpronos",
                0
            ),

            x.get(
                "best_pick",
                {}
            ).get(
                "confidence",
                0
            )
        ),
        reverse=True
    )


def build_top10(matches):

    ranked = rank_matches(
        matches
    )

    top10 = ranked[
        :MAX_MATCHES
    ]

    result = []

    for index, match in enumerate(
        top10,
        start=1
    ):

        row = {

            "rank":
                index,

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

            "match":
                f"{match.get('home_team')} vs {match.get('away_team')}",

            "score_xpronos":
                match.get(
                    "score_xpronos"
                ),

            "active":
                True,

            "status":
                "ACTIF ✅",

            "best_pick":
                match.get(
                    "best_pick"
                ),

            "second_pick":
                match.get(
                    "second_pick"
                ),

            "best_exact_score":
                match.get(
                    "best_exact_score"
                )
        }

        result.append(
            row
        )

    return result


def main():

    matches = load_matches()

    top10 = build_top10(
        matches
    )

    output = {

        "engine":
            "MRXPRONOS_V4",

        "generated_at":
            datetime.utcnow().isoformat(),

        "count":
            len(top10),

        "matches":
            top10
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
        f"🏆 TOP {len(top10)} généré"
    )


if __name__ == "__main__":
    main()
