def build_top10(matches):

    active = [
        m
        for m in matches
        if m["active"]
    ]

    active.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return active[:
  10]
