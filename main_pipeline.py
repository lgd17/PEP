#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main_pipeline.py

Pipeline complet MR XPRONOS V4
"""

import subprocess
import sys
from pathlib import Path


PIPELINE = [

    "fetch_today_matches.py",

    "prefilter_candidates.py",

    "h2h_service.py",

    "form_service.py",

    "standings_service.py",

    "injuries_service.py",

    "odds_service.py",

    "xg_service.py",

    "xpronos_score_engine.py",

    "market_engine.py",

    "active_filter.py",

    "top10_builder.py",

    "logo_service.py",

    "image_renderer.py"
]


def run_script(script):

    print(
        "\n" +
        "=" * 60
    )

    print(
        f"🚀 Exécution : {script}"
    )

    print(
        "=" * 60
    )

    result = subprocess.run(
        [sys.executable, script]
    )

    if result.returncode != 0:

        print(
            f"❌ Erreur dans {script}"
        )

        raise SystemExit(
            result.returncode
        )

    print(
        f"✅ {script}"
    )


def verify_outputs():

    required = [

        Path(
            "data/top10_active.json"
        ),

        Path(
            "output/top10.png"
        )
    ]

    missing = [

        str(p)

        for p in required

        if not p.exists()
    ]

    if missing:

        print(
            "❌ Fichiers manquants :"
        )

        for file in missing:

            print(
                f"   - {file}"
            )

        raise SystemExit(1)

    print(
        "\n✅ Vérification terminée"
    )


def main():

    print(
        "\n🏆 MR XPRONOS V4"
    )

    print(
        "Analyse automatique des matchs\n"
    )

    for script in PIPELINE:

        run_script(
            script
        )

    verify_outputs()

    print(
        "\n🎯 TOP 10 ACTIF généré"
    )

    print(
        "📄 data/top10_active.json"
    )

    print(
        "🖼 output/top10.png"
    )

    print(
        "\n✅ PIPELINE TERMINÉ"
    )


if __name__ == "__main__":
    main()
