from api_utils import make_request

API = "https://v2.football.sportsapipro.com"

def get_h2h(match_id):

    resp = make_request(
        "GET",
        f"{API}/api/match/{match_id}/h2h"
    )

    if not resp:
        return {}

    return resp.j
son()
