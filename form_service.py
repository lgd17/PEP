from api_utils import make_request

API = "https://v2.football.sportsapipro.com"

def get_form(match_id):

    resp = make_request(
        "GET",
        f"{API}/api/match/{match_id}/pregame-form"
    )

    if not resp:
        return {}

    return resp.j
son()
