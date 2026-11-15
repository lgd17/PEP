#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
telegram_publisher.py

Publication Telegram MR XPRONOS V4
"""

import json
import os
from pathlib import Path

import requests

TOKEN = os.getenv(
    "FOOTBALL_NEWS_BOT_TOKEN"
)

CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)

IMAGE_FILE = "output/top10.png"

JSON_FILE = "data/top10_active.json"


def load_top10():

    path = Path(JSON_FILE)

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


def build_caption(matches):

    lines = [

        "🏆 MR XPRONOS - TOP 10 ACTIF",
        ""
    ]

    for match in matches[:5]:

        market = (
            match.get(
                "best_pick",
                {}
            )
        )

        score = (
            match.get(
                "best_exact_score",
                {}
            )
        )

        lines.extend([

            f"⚽ {match['home_team']} vs {match['away_team']}",

            f"✅ {market.get('market','-')} ({market.get('confidence',0)}%)",

            f"🎯 Score : {score.get('score','-')}",

            ""
        ])

    lines.append(
        "📊 Analyse MR XPRONOS V4"
    )

    return "\n".join(lines)


def send_photo(caption):

    if not TOKEN:
        raise ValueError(
            "FOOTBALL_NEWS_BOT_TOKEN manquant"
        )

    if not CHAT_ID:
        raise ValueError(
            "TELEGRAM_CHAT_ID manquant"
        )

    photo = Path(IMAGE_FILE)

    if not photo.exists():

        raise FileNotFoundError(
            IMAGE_FILE
        )

    url = (
        f"https://api.telegram.org"
        f"/bot{TOKEN}/sendPhoto"
    )

    with open(
        photo,
        "rb"
    ) as image:

        response = requests.post(

            url,

            data={
                "chat_id": CHAT_ID,
                "caption": caption
            },

            files={
                "photo": image
            },

            timeout=60
        )

    if response.status_code != 200:

        raise RuntimeError(
            response.text
        )

    return response.json()


def main():

    matches = load_top10()

    if not matches:

        print(
            "⚠️ Aucun match actif"
        )

        return

    caption = build_caption(
        matches
    )

    result = send_photo(
        caption
    )

    print(
        "✅ Publication Telegram"
    )

    print(
        result
    )


if __name__ == "__main__":
    main()
