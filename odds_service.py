from api_utils import make_request

API = "https://v2.football.sportsapipro.com"

def get_odds(match_id):

    resp = make_request(
        "GET",
        f"{API}/api/match/{match_id}/odds/pre-match"
    )

    if not resp:
        return {}

    return resp.j
  son()
