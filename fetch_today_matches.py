#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fetch_today_matches.py

Récupère tous les matchs du jour depuis SportsAPI Pro
et les sauvegarde dans data/today_matches.json
"""

import json
import os
from datetime import datetime

from api_utils import make_request

BASE_URL = "https://v2.football.sportsapipro.com"

OUTPUT_FILE = "data/today_matches.json"


def fetch_today_matches():

    print("⚽ Récupération des matchs du jour...")

    response = make_request(
        "GET",
        f"{BASE_URL}/api/today"
    )

    if response is None:
        print("❌ Impossible de récupérer les matchs.")
        return False

    payload = response.json()

    matches = payload.get("events", [])

    result = {
        "generated_at": datetime.utcnow().isoformat(),
        "count": len(matches),
        "matches": matches
    }

    os.makedirs("data", exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            result,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"✅ {len(matches)} matchs enregistrés dans {OUTPUT_FILE}"
    )

    return True


if __name__ == "__main__":
    fetch_today_matches()
