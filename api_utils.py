#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
api_utils.py

Module central des requêtes SportsAPI Pro.
Gestion :
- clé API
- timeout
- retry simple
- erreurs HTTP
"""

import os
import time
import requests

BASE_HEADERS = {
    "Accept": "application/json"
}

API_KEY = os.getenv("SPORTDATA_API_KEY")

if not API_KEY:
    raise ValueError(
        "SPORTDATA_API_KEY non défini"
    )


def make_request(
    method,
    url,
    params=None,
    timeout=30,
    retries=2
):

    headers = BASE_HEADERS.copy()

    headers["x-api-key"] = API_KEY

    for attempt in range(retries + 1):

        try:

            response = requests.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                timeout=timeout
            )

            if response.status_code == 200:
                return response

            print(
                f"HTTP {response.status_code} : {url}"
            )

            if response.status_code >= 500:
                return None

        except requests.RequestException as e:

            print(
                f"Erreur API : {e}"
            )

        if attempt < retries:

            time.sleep
(2)

    return None
