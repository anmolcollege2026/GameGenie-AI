"""
GameGenie AI
LLM Parser

This module uses Gemini to understand the user's
natural-language game request.

It extracts:
    - genre
    - mood
    - platform
    - multiplayer
    - difficulty
    - playtime
    - database search queries
"""

import json

from google import genai

from config import GEMINI_API_KEY


# -----------------------------------------
# Gemini client
# -----------------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# -----------------------------------------
# Extract preferences
# -----------------------------------------

def extract_preferences(user_prompt: str) -> dict:

    prompt = f"""
You are an expert video game recommendation assistant.

Analyze the user's request.

Return ONLY valid JSON.

Do not explain anything.

Do not use markdown.

The JSON must contain:

{{
    "genre": "",
    "mood": "",
    "platform": "",
    "multiplayer": false,
    "difficulty": "",
    "playtime": "",
    "search_queries": []
}}

The search_queries field must contain exactly
3 concise search queries useful for searching
a video game database.

The search queries should combine important concepts.

Example:

User:
"I want a relaxing farming game for PC"

Good queries:

[
    "farming simulator",
    "cozy farming",
    "farming life simulation"
]

Bad queries:

[
    "relaxing",
    "PC",
    "cozy"
]

User Request:

{user_prompt}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    try:

        return json.loads(response.text)

    except Exception:

        return {
            "genre": "Unknown",
            "mood": "Unknown",
            "platform": "Any",
            "multiplayer": False,
            "difficulty": "Any",
            "playtime": "Any",
            "search_queries": [
                "popular games",
                "indie games",
                "adventure games"
            ]
        }