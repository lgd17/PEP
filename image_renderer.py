#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
image_renderer.py

Génère le visuel Telegram
à partir de top10_active.json

Sortie :
    output/top10.png
"""

import json
from pathlib import Path

from PIL import (
    Image,
    ImageDraw,
    ImageFont
)


INPUT_FILE = "data/top10_active.json"

OUTPUT_FILE = "output/top10.png"

LOGO_DIR = Path(
    "cache/logos"
)


WIDTH = 1080

CARD_HEIGHT = 260

MARGIN = 20


def load_top10():

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


def load_font(size):

    try:

        return ImageFont.truetype(
            "DejaVuSans-Bold.ttf",
            size
        )

    except Exception:

        return ImageFont.load_default()


def open_logo(team_id):

    logo = (
        LOGO_DIR /
        f"{team_id}.png"
    )

    if not logo.exists():
        return None

    try:

        image = Image.open(
            logo
        ).convert(
            "RGBA"
        )

        image.thumbnail(
            (110, 110)
        )

        return image

    except Exception:

        return None


def draw_match_card(
    draw,
    canvas,
    match,
    y
):

    draw.rounded_rectangle(

        (
            20,
            y,
            WIDTH - 20,
            y + CARD_HEIGHT
        ),

        radius=25,

        fill="#0F172A"
    )

    rank_font = load_font(
        44
    )

    title_font = load_font(
        36
    )

    small_font = load_font(
        28
    )

    draw.text(

        (40, y + 20),

        f"#{match['rank']}",

        fill="gold",

        font=rank_font
    )

    draw.text(

        (170, y + 25),

        f"{match['home_team']} vs {match['away_team']}",

        fill="white",

        font=title_font
    )

    home_logo = open_logo(
        match.get(
            "home_team_id"
        )
    )

    away_logo = open_logo(
        match.get(
            "away_team_id"
        )
    )

    if home_logo:

        canvas.paste(

            home_logo,

            (60, y + 90),

            home_logo
        )

    if away_logo:

        canvas.paste(

            away_logo,

            (WIDTH - 180, y + 90),

            away_logo
        )

    best = (
        match.get(
            "best_pick",
            {}
        )
    )

    second = (
        match.get(
            "second_pick",
            {}
        )
    )

    exact = (
        match.get(
            "best_exact_score",
            {}
        )
    )

    draw.text(

        (220, y + 95),

        f"✅ {best.get('market','-')}  ({best.get('confidence',0)}%)",

        fill="#00ff99",

        font=small_font
    )

    draw.text(

        (220, y + 135),

        f"✅ {second.get('market','-')}  ({second.get('confidence',0)}%)",

        fill="#00d2ff",

        font=small_font
    )

    draw.text(

        (220, y + 180),

        f"🎯 Score : {exact.get('score','-')}",

        fill="orange",

        font=small_font
    )

    draw.text(

        (800, y + 180),

        f"XP : {match.get('score_xpronos',0)}",

        fill="white",

        font=small_font
    )


def main():

    matches = load_top10()

    count = len(
        matches
    )

    height = (

        120 +

        (

            CARD_HEIGHT +
            MARGIN

        ) * count
    )

    canvas = Image.new(

        "RGB",

        (
            WIDTH,
            height
        ),

        "#020617"
    )

    draw = ImageDraw.Draw(
        canvas
    )

    title_font = load_font(
        52
    )

    draw.text(

        (30, 25),

        "MR XPRONOS - TOP 10 ACTIF",

        fill="gold",

        font=title_font
    )

    y = 110

    for match in matches:

        draw_match_card(

            draw,

            canvas,

            match,

            y
        )

        y += (

            CARD_HEIGHT +
            MARGIN
        )

    Path(
        "output"
    ).mkdir(
        exist_ok=True
    )

    canvas.save(
        OUTPUT_FILE
    )

    print(
        f"✅ {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
  
