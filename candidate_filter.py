def filter_candidates(matches):

    candidates = []

    for match in matches:

        status = match.get("status")

        if status not in (
            "notstarted",
            "scheduled"
        ):
            continue

        candidates.append(match)

    return candidate
  s[:15]
