"""
GameGenie AI
IGDB Service

This module communicates with the IGDB API.

Responsibilities:
1. Authenticate with Twitch
2. Search IGDB for games
3. Return useful game information

It does NOT decide which game is best.
That will be our ranking algorithm.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")


def get_access_token():
    """
    Get an access token from Twitch.

    IGDB uses Twitch authentication before
    allowing us to access the game database.
    """

    url = "https://id.twitch.tv/oauth2/token"

    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, params=params)

    response.raise_for_status()

    data = response.json()

    return data["access_token"]


def search_games(search_term, limit=10):
    """
    Search IGDB for games.

    Args:
        search_term (str):
            Words describing the games we want.

        limit (int):
            Maximum number of games to return.

    Returns:
        list:
            List of game dictionaries.
    """

    access_token = get_access_token()

    url = "https://api.igdb.com/v4/games"

    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }

    query = f"""
        search "{search_term}";
        fields
            name,
            summary,
            rating,
            total_rating,
            first_release_date,
            cover.url,
            genres.name,
            themes.name,
            game_modes.name,
            platforms.name;
        limit {limit};
    """

    response = requests.post(
        url,
        headers=headers,
        data=query
    )

    response.raise_for_status()

    return response.json()
def search_multiple_terms(search_terms, limit_per_term=10):
    """
    Search IGDB using several natural-language queries.

    Gemini generates the queries.
    This function expands them into useful search terms,
    queries IGDB, and removes duplicate games.
    """

    all_games = {}

    # Words that usually don't help IGDB search
    stop_words = {
        "a",
        "an",
        "the",
        "and",
        "or",
        "for",
        "with",
        "game",
        "games",
        "single",
        "player",
        "play",
        "playing",
        "that",
        "want",
        "like"
    }

    expanded_terms = []

    for term in search_terms:

        if not term:
            continue

        term = term.strip()

        # 1. Original Gemini query
        expanded_terms.append(term)

        words = term.lower().split()

        # 2. Important individual concepts
        for word in words:

            if (
                len(word) >= 5
                and word not in stop_words
            ):
                expanded_terms.append(word)

        # 3. Two-word combinations
        useful_words = [
            word
            for word in words
            if word not in stop_words
        ]

        for i in range(len(useful_words) - 1):

            pair = (
                useful_words[i]
                + " "
                + useful_words[i + 1]
            )

            expanded_terms.append(pair)

    # Remove duplicates
    unique_terms = []

    for term in expanded_terms:

        term = term.strip().lower()

        if (
            term
            and term not in unique_terms
        ):
            unique_terms.append(term)

    # Search IGDB
    for term in unique_terms:

        try:

            games = search_games(
                term,
                limit=limit_per_term
            )

            for game in games:

                game_id = game.get("id")

                if game_id is not None:

                    all_games[game_id] = game

        except requests.RequestException:
            continue

    return list(all_games.values())