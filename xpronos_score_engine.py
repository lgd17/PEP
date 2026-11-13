#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mr XPRONOS V4
Moteur principal de notation
"""

MIN_CONFIDENCE = 80


def normalize(value, minimum, maximum):

    if maximum <= minimum:
        return 50

    score = (
        (value - minimum)
        /
        (maximum - minimum)
    ) * 100

    return max(0, min(100, score))


def compute_xpronos_score(
    h2h_score,
    form_score,
    ranking_score,
    injuries_score,
    odds_score,
    xg_score
):

    # POIDS

    H2H_WEIGHT = 0.15

    FORM_WEIGHT = 0.25

    RANK_WEIGHT = 0.15

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
xpronos_score_engine.py

Fusionne toutes les analyses
et produit le Score XPRONOS.

Sortie :
    data/detailed_analysis.json
"""

import json
from pathlib import Path


DATA_DIR = Path("data")

OUTPUT_FILE = DATA_DIR / "detailed_analysis.json"


# Poids principaux

WEIGHTS = {

    "h2h_score": 0.15,

    "form_score": 0.25,

    "ranking_score": 0.15,

    "injuries_score": 0.10,

    "odds_score": 0.20,

    "xg_score": 0.15
}


def load_analysis(filename):

    path = DATA_DIR / filename

    if not path.exists():
        return {}

    payload = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    result = {}

    for row in payload.get(
        "matches",
        []
    ):

        result[
            row["match_id"]
        ] = row

    return result


def compute_score(match):

    total = 0

    for field, weight in WEIGHTS.items():

        total += (

            match.get(
                field,
                50
            )

            * weight
        )

    return round(
        total,
        2
    )


def merge_match_data():

    h2h = load_analysis(
        "h2h_analysis.json"
    )

    form = load_analysis(
        "form_analysis.json"
    )

    standings = load_analysis(
        "standings_analysis.json"
    )

    injuries = load_analysis(
        "injuries_analysis.json"
    )

    odds = load_analysis(
        "odds_analysis.json"
    )

    xg = load_analysis(
        "xg_analysis.json"
    )

    match_ids = set()

    for source in (
        h2h,
        form,
        standings,
        injuries,
        odds,
        xg
    ):
        match_ids.update(
            source.keys()
        )

    results = []

    for match_id in match_ids:

        merged = {

            "match_id": match_id
        }

        merged.update(
            h2h.get(
                match_id,
                {}
            )
        )

        merged.update(
            form.get(
                match_id,
                {}
            )
        )

        merged.update(
            standings.get(
                match_id,
                {}
            )
        )

        merged.update(
            injuries.get(
                match_id,
                {}
            )
        )

        merged.update(
            odds.get(
                match_id,
                {}
            )
        )

        merged.update(
            xg.get(
                match_id,
                {}
            )
        )

        merged[
            "score_xpronos"
        ] = compute_score(
            merged
        )

        results.append(
            merged
        )

    return results


def build_summary(results):

    if not results:

        return {}

    scores = [

        x["score_xpronos"]

        for x in results
    ]

    return {

        "matches_analyzed":
            len(results),

        "best_score":
            max(scores),

        "worst_score":
            min(scores),

        "average_score":
            round(
                sum(scores)
                /
                len(scores),
                2
            )
    }


def main():

    results = merge_match_data()

    results.sort(

        key=lambda x:

        x["score_xpronos"],

        reverse=True
    )

    output = {

        "engine":

        "MRXPRONOS_V4",

        "weights":

        WEIGHTS,

        "summary":

        build_summary(
            results
        ),

        "matches":

        results
    }

    OUTPUT_FILE.write_text(

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
        f"📊 Matchs analysés : {len(results)}"
    )


if __name__ == "__main__":
    main()

arket_factor * 0.20
    )

    return round(
        confidence,
        2
    )


def market_active(
    confidence,
    odds,
    min_odds,
    max_odds
):
    return (

        confidence >= 80

        and

       
min_odds <= odds <= max_odds
    )
