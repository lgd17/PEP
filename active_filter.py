def is_active(
    confidence,
    odds
):

    return (
        confidence >= 70
        and
        1.40 <= odds <= 2.00
    )
      
