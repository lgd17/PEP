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

    INJURY_WEIGHT = 0.10

    ODDS_WEIGHT = 0.20

    XG_WEIGHT = 0.15

    final_score = (

        h2h_score * H2H_WEIGHT +

        form_score * FORM_WEIGHT +

        ranking_score * RANK_WEIGHT +

        injuries_score * INJURY_WEIGHT +

        odds_score * ODDS_WEIGHT +

        xg_score * XG_WEIGHT
    )

    return round(final_score, 2)


def market_confidence(
    xpronos_score,
    market_factor
):

    confidence = (

        xpronos_score * 0.80 +

        market_factor * 0.20
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
