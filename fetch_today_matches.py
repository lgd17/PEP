from api_utils import make_request

API = "https://v2.football.sportsapipro.com"

def fetch_matches():

    resp = make_request(
        "GET",
        f"{API}/api/today"
    )

    if not resp:
        return []

    data = resp.json()

    return data.get("events
      ", [])
