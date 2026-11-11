from fetch_today_matches import fetch_matches
from candidate_filter import filter_candidates
from active_filter import is_active
from top10_builder import build_top10

matches = fetch_matches()

candidates = filter_candidates(matches)

results = []

for match in candidates:

    confidence = 78
    odds = 1.65

    results.append({
        "match":
            f"{match.get('homeTeam')} vs {match.get('awayTeam')}",
        "confidence":
            confidence,
        "odds":
            odds,
        "active":
            is_active(
                confidence,
                odds
            )
    })

top10 = build_top10(results)

for row in top10:

    print(
        row["match"],
        row["confidence"],
        "ACTIF
✅"
    )
