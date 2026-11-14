#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
logo_service.py

Télécharge et met en cache
les logos des clubs.

Entrée :
    data/top10_active.json

Sortie :
    cache/logos/*.png
"""

import json
from pathlib import Path

import requests

from api_utils import make_request

BASE_URL = "https://v2.football.sportsapipro.com"

INPUT_FILE = "data/top10_active.json"

CACHE_DIR = Path(
    "cache/logos"
)


def load_matches():

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


def fetch_logo_url(team_id):

    response = make_request(

        "GET",

        f"{BASE_URL}/api/teams/{team_id}/image"
    )

    if response is None:

        return None

    try:

        payload = response.json()

        return (

            payload.get("image")

            or

            payload.get("url")

            or

            payload.get("logo")

        )

    except Exception:

        return None


def download_logo(
    team_id,
    image_url
):

    CACHE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    destination = (

        CACHE_DIR /
        f"{team_id}.png"
    )

    if destination.exists():

        print(
            f"✅ Cache logo {team_id}"
        )

        return destination

    try:

        response = requests.get(

            image_url,

            timeout=20
        )

        if response.status_code != 200:

            return None

        destination.write_bytes(
            response.content
        )

        print(
            f"⬇️ Logo téléchargé : {team_id}"
        )

        return destination

    except Exception:

        return None


def process_team(team_id):

    if not team_id:
        return

    cached = (

        CACHE_DIR /
        f"{team_id}.png"
    )

    if cached.exists():

        return

    image_url = fetch_logo_url(
        team_id
    )

    if not image_url:

        print(
            f"⚠️ Aucun logo trouvé : {team_id}"
        )

        return

    download_logo(
        team_id,
        image_url
    )


def main():

    matches = load_matches()

    for match in matches:

        home_id = match.get(
            "home_team_id"
        )

        away_id = match.get(
            "away_team_id"
        )

        process_team(
            home_id
        )

        process_team(
            away_id
        )

    print(
        "✅ Tous les logos disponibles"
    )


if __name__ == "__main__":
    main()
