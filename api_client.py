import os
import requests

from logger import logger
from models import MovementsResponse, PlayerResponse

X_LEAGUE_HEADER = os.getenv("X_LEAGUE_HEADER")
X_LEAGUE_HEADER_VALUE = os.getenv("X_LEAGUE_HEADER_VALUE")
X_USER_HEADER = os.getenv("X_USER_HEADER")
X_USER_HEADER_VALUE = os.getenv("X_USER_HEADER_VALUE")

BIW_USERNAME = os.getenv("BIW_USERNAME")
BIW_PASSWORD = os.getenv("BIW_PASSWORD")

GET_TOKEN_URL = os.getenv("GET_TOKEN_URL")
MOVEMENTS_URL = os.getenv("GET_CLAUSES_MOVEMENTS_URL")
MOVEMENTS_URL = MOVEMENTS_URL.replace("$League_Id", X_LEAGUE_HEADER_VALUE)

GET_PLAYER_DETAIL = os.getenv("GET_PLAYER_DETAIL")


class ApiError(RuntimeError):
    pass


def get_biwenger_token() -> str | None:
    body = {"email":BIW_USERNAME, "password":BIW_PASSWORD}
    response = requests.post(GET_TOKEN_URL, json=body)
    if response.ok:
        logger.info("Login done!")
        return response.json()["token"]
    else:
        logger.info("Error: " + response.text)
        return None


def get_clause_movements(token: str) -> MovementsResponse:
    if token is None:
        raise ApiError("Token not provided")

    resp = requests.get(MOVEMENTS_URL, headers=generate_headers(token))
    mv = MovementsResponse.model_validate(resp.json())

    if mv.status != 200:
        raise ApiError(f"API status != 200: {mv.status}")
    logger.info("Movements found!")
    return mv


def get_player_detail(player_id: int, token: str) -> PlayerResponse | None:
    if token is None:
        raise ApiError("Token not provided")

    response = requests.get(GET_PLAYER_DETAIL + str(player_id), headers=generate_headers(token))
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise ApiError(f"HTTP {response.status_code}: {response.text[:200]}") from e

    if response.ok:
        logger.info("Player found!")
        return PlayerResponse.model_validate(response.json(), strict=False)
    else:
        logger.info("Error: " + response.text)
        return None

def generate_headers(token : str) -> dict[str, str]:
    return {
        "Authorization": "Bearer " + token,
        X_LEAGUE_HEADER : X_LEAGUE_HEADER_VALUE,
        X_USER_HEADER : X_USER_HEADER_VALUE
    }