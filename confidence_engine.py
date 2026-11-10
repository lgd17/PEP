def calculate_confidence(
    form_score,
    h2h_score,
    ranking_score,
    odds_score,
    injury_score
):

    score = (
        form_score * 0.30 +
        h2h_score * 0.20 +
        ranking_score * 0.15 +
        odds_score * 0.20 +
        injury_score * 0.15
    )

    return round(score, 
      2)
