#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
prefilter_candidates.py

Réduit le nombre de matchs à analyser
de 40 à environ 15 candidats.

Aucune requête API.
Travaille uniquement sur today_matches.json
"""

import json
from pathlib import Path

INPUT_FILE = "data/today_matches.json"

OUTPUT_FILE = "data/candidates.json"

MAX_CANDIDATES = 15


def get_filter_score(match):

    score = 0

    tournament = str(
        match.get("tournament", {})
        .get("name", "")
    ).lower()

    # Compétitions majeures

    important_leagues = [

        "premier",
        "liga",
        "bundesliga",
        "serie a",
        "ligue 1",
        "champions",
        "europa"
    ]

    for league in important_leagues:

        if league in tournament:

            score += 20

            break

    # Match programmé

    status = str(
        match.get("status", {})
        .get("type", "")
    ).lower()

    if status in (
        "notstarted",
        "scheduled"
    ):
        score += 15

    # Match avec identifiant valide

    if match.get("id"):
        score += 10

    return score


def main():

    path = Path(INPUT_FILE)

    if not path.exists():

        print(
            f"❌ {INPUT_FILE} introuvable"
        )

        return

    data = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    matches = data.get(
        "matches",
        []
    )

    ranked = []

    for match in matches:

        ranked.append(
            {
                "score": get_filter_score(match),
                "match": match
            }
        )

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    selected = [

        row["match"]

        for row in ranked[:MAX_CANDIDATES]
    ]

    output = {

        "source_matches": len(matches),

        "selected_matches": len(selected),

        "matches": selected
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
        f"✅ {len(selected)} candidats enregistrés"
    )

    print(
        f"📁 {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
