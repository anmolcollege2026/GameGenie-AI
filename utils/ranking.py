"""
GameGenie AI
Robust Generic Game Ranking Engine

Gemini extracts the user's preferences.
This module independently scores and ranks games.

Design goals:
- Work with a very large variety of genres/subgenres.
- Avoid returning zero recommendations simply because a
  user entered a genre that is not explicitly listed.
- Use IGDB metadata whenever available.
- Use natural-language evidence as a fallback.
- Keep recommendations explainable.
"""

import re


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text):
    """Normalize text for matching."""

    if text is None:
        return ""

    text = str(text).lower()

    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = text.replace("/", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text):
    """Return useful normalized words."""

    text = normalize_text(text)

    return {
        word
        for word in re.findall(r"[a-z0-9]+", text)
        if len(word) >= 3
    }


# ============================================================
# GAME TEXT
# ============================================================

def get_game_text(game):
    """
    Combine as much searchable IGDB information as possible.
    """

    parts = []

    parts.append(
        game.get("name", "")
    )

    parts.append(
        game.get("summary", "")
    )

    parts.append(
        game.get("storyline", "")
    )

    for genre in game.get("genres", []):
        parts.append(
            genre.get("name", "")
        )

    for theme in game.get("themes", []):
        parts.append(
            theme.get("name", "")
        )

    for keyword in game.get("keywords", []):
        if isinstance(keyword, dict):
            parts.append(
                keyword.get("name", "")
            )
        else:
            parts.append(
                str(keyword)
            )

    return normalize_text(
        " ".join(
            str(part)
            for part in parts
            if part
        )
    )


# ============================================================
# GENRE / SUBGENRE SYNONYMS
# ============================================================

GENRE_SYNONYMS = {

    "rpg": {
        "rpg",
        "role playing",
        "role playing game",
        "role playing games",
        "role playing video game",
        "jrpg",
        "crpg",
        "arpg",
        "action rpg",
        "action role playing",
        "tactical rpg",
        "strategy rpg",
        "turn based rpg",
        "mmorpg",
    },

    "action": {
        "action",
        "action game",
        "combat",
        "hack slash",
        "hack and slash",
        "beat em up",
        "fighting",
    },

    "adventure": {
        "adventure",
        "adventure game",
        "exploration",
        "exploration game",
        "walking simulator",
    },

    "shooter": {
        "shooter",
        "shooting",
        "fps",
        "first person shooter",
        "third person shooter",
        "tps",
        "twin stick shooter",
        "bullet hell",
        "arena shooter",
    },

    "platformer": {
        "platformer",
        "platform game",
        "platforming",
        "2d platformer",
        "3d platformer",
        "precision platformer",
    },

    "puzzle": {
        "puzzle",
        "puzzle game",
        "logic puzzle",
        "jigsaw",
        "brain game",
    },

    "strategy": {
        "strategy",
        "strategic",
        "strategy game",
        "tactical",
        "tactical game",
        "turn based strategy",
        "rts",
        "real time strategy",
        "grand strategy",
        "4x",
        "tower defense",
        "tower defence",
    },

    "simulation": {
        "simulation",
        "simulator",
        "sim",
        "simulation game",
        "management",
        "management game",
        "life simulation",
        "social simulation",
        "vehicle simulation",
        "business simulation",
    },

    "farming": {
        "farming",
        "farm",
        "farm simulation",
        "farming simulation",
        "agriculture",
        "farming game",
        "crop",
        "harvest",
    },

    "fashion": {
        "fashion",
        "fashion game",
        "fashion simulation",
        "dress up",
        "dress up game",
        "styling",
        "clothing",
        "outfit",
        "makeover",
        "wardrobe",
    },

    "racing": {
        "racing",
        "racing game",
        "driving",
        "driving game",
        "car racing",
        "kart racing",
        "arcade racing",
        "sim racing",
    },

    "sports": {
        "sports",
        "sport",
        "football",
        "soccer",
        "basketball",
        "baseball",
        "tennis",
        "golf",
        "hockey",
        "boxing",
        "wrestling",
    },

    "horror": {
        "horror",
        "survival horror",
        "psychological horror",
        "horror game",
        "scary",
    },

    "survival": {
        "survival",
        "survival game",
        "survival crafting",
        "crafting survival",
    },

    "sandbox": {
        "sandbox",
        "sandbox game",
        "open ended",
        "open world",
        "player driven",
    },

    "roguelike": {
        "roguelike",
        "rogue like",
        "roguelite",
        "rogue lite",
        "rogue like game",
    },

    "metroidvania": {
        "metroidvania",
        "metroid vania",
    },

    "visual novel": {
        "visual novel",
        "visual novels",
        "vn",
        "interactive novel",
    },

    "dating sim": {
        "dating sim",
        "dating simulation",
        "romance simulation",
        "dating game",
    },

    "card game": {
        "card game",
        "cards",
        "deckbuilder",
        "deck builder",
        "collectible card game",
        "ccg",
        "trading card game",
        "tcg",
    },

    "board game": {
        "board game",
        "board games",
        "tabletop",
        "tabletop game",
    },

    "music": {
        "music game",
        "rhythm game",
        "rhythm",
        "music",
    },

    "party": {
        "party game",
        "party games",
        "social game",
        "local multiplayer party",
    },

    "fighting": {
        "fighting game",
        "fighting",
        "fighter",
        "one on one fighting",
    },

    "stealth": {
        "stealth",
        "stealth game",
        "infiltration",
        "sneaking",
    },

    "mmo": {
        "mmo",
        "mmorpg",
        "massively multiplayer",
        "massively multiplayer online",
    },

    "mmorpg": {
        "mmorpg",
        "massively multiplayer online role playing",
        "online role playing",
    },

    "city builder": {
        "city builder",
        "city building",
        "city building game",
        "urban planning",
        "city simulation",
    },

    "building": {
        "building",
        "construction",
        "builder",
        "building game",
        "construction game",
    },

    "crafting": {
        "crafting",
        "crafting game",
        "craft",
        "resource crafting",
    },

    "cooking": {
        "cooking",
        "cooking game",
        "restaurant simulation",
        "chef game",
        "food simulation",
    },

    "fishing": {
        "fishing",
        "fishing game",
        "fishing simulator",
    },

    "dating": {
        "dating",
        "dating game",
        "romance",
        "romantic simulation",
    },

    "educational": {
        "educational",
        "education",
        "learning game",
        "educational game",
    },

    "arcade": {
        "arcade",
        "arcade game",
    },

    "casual": {
        "casual",
        "casual game",
    },

    "indie": {
        "indie",
        "independent game",
    },

    "narrative": {
        "narrative",
        "story driven",
        "story driven game",
        "story rich",
        "interactive story",
    },

    "text adventure": {
        "text adventure",
        "text based adventure",
        "interactive fiction",
    },

    "strategy rpg": {
        "strategy rpg",
        "tactical rpg",
        "tactics rpg",
        "srpg",
    },

    "turn based": {
        "turn based",
        "turn based game",
        "turnbased",
    },

    "real time": {
        "real time",
        "real time game",
        "real time strategy",
    },

    "action adventure": {
        "action adventure",
        "action adventure game",
    },

    "first person": {
        "first person",
        "first person game",
        "fps",
    },

    "third person": {
        "third person",
        "third person game",
        "tps",
    },

    "mobile": {
        "mobile",
        "mobile game",
        "android game",
        "ios game",
    },
}


# ============================================================
# MOOD VOCABULARY
# ============================================================

MOOD_WORDS = {

    "relaxing": {
        "relaxing",
        "relaxed",
        "cozy",
        "peaceful",
        "calm",
        "chill",
        "wholesome",
        "laid back",
    },

    "creative": {
        "creative",
        "creativity",
        "create",
        "creating",
        "design",
        "designing",
        "customize",
        "customization",
        "building",
        "fashion",
        "styling",
        "dress up",
        "dress up",
        "makeover",
    },

    "dark": {
        "dark",
        "horror",
        "survival",
        "thriller",
        "scary",
        "grim",
        "gloomy",
        "disturbing",
    },

    "challenging": {
        "hard",
        "difficult",
        "challenging",
        "souls like",
        "soulslike",
        "hardcore",
        "punishing",
    },

    "funny": {
        "funny",
        "humorous",
        "comedy",
        "comedic",
        "silly",
        "absurd",
    },

    "cute": {
        "cute",
        "adorable",
        "wholesome",
        "charming",
        "colorful",
    },

    "serious": {
        "serious",
        "dramatic",
        "realistic",
        "mature",
    },

    "epic": {
        "epic",
        "grand",
        "massive",
        "cinematic",
        "heroic",
    },

    "romantic": {
        "romantic",
        "romance",
        "love",
        "dating",
        "relationship",
    },
}


# ============================================================
# GENRE GROUP DETECTION
# ============================================================

def get_genre_group(preference):
    """
    Find the closest known conceptual genre group.
    """

    preference = normalize_text(
        preference
    )

    if not preference:
        return None

    # Exact conceptual match
    for group, values in GENRE_SYNONYMS.items():

        if preference == group:
            return group

        if preference in values:
            return group

    # Phrase containment
    for group, values in GENRE_SYNONYMS.items():

        for value in values:

            if (
                value in preference
                or preference in value
            ):
                return group

    return None


# ============================================================
# GENRE MATCH SCORE
# ============================================================

def genre_match_score(preference, game):
    """
    Return a genre relevance score from 0 to 40.

    This deliberately does NOT require a perfect dictionary match.
    """

    preference = normalize_text(
        preference
    )

    if not preference:
        return 20

    game_genres = [
        normalize_text(
            genre.get("name", "")
        )
        for genre in game.get(
            "genres",
            []
        )
    ]

    game_text = get_game_text(
        game
    )

    # --------------------------------------------------------
    # Exact IGDB genre match
    # --------------------------------------------------------

    for genre in game_genres:

        if preference == genre:
            return 40

        if (
            preference in genre
            or genre in preference
        ):
            return 38

    # --------------------------------------------------------
    # Known synonym group
    # --------------------------------------------------------

    requested_group = get_genre_group(
        preference
    )

    if requested_group:

        synonyms = GENRE_SYNONYMS[
            requested_group
        ]

        for genre in game_genres:

            if genre in synonyms:
                return 38

            for synonym in synonyms:

                if (
                    synonym in genre
                    or genre in synonym
                ):
                    return 36

        # Search description / themes / keywords
        matching_terms = sum(
            1
            for synonym in synonyms
            if synonym in game_text
        )

        if matching_terms >= 2:
            return 34

        if matching_terms == 1:
            return 28

    # --------------------------------------------------------
    # Natural-language fallback
    # --------------------------------------------------------

    preference_tokens = tokenize(
        preference
    )

    if preference_tokens:

        game_tokens = tokenize(
            game_text
        )

        overlap = (
            preference_tokens
            & game_tokens
        )

        ratio = (
            len(overlap)
            / len(preference_tokens)
        )

        if ratio >= 0.75:
            return 32

        if ratio >= 0.5:
            return 26

        if ratio > 0:
            return 18

    # --------------------------------------------------------
    # Unknown genre fallback
    #
    # We don't completely eliminate the game.
    # --------------------------------------------------------

    return 10


# ============================================================
# GENRE MATCH BOOLEAN
# ============================================================

def genre_match(preference, game):
    """
    Compatibility helper.

    A game is considered relevant if it receives meaningful
    genre evidence.
    """

    return (
        genre_match_score(
            preference,
            game
        ) >= 18
    )


# ============================================================
# MOOD MATCH
# ============================================================

def get_mood_group(preference):
    """Return the closest mood group."""

    preference = normalize_text(
        preference
    )

    if not preference:
        return None

    for mood, words in MOOD_WORDS.items():

        if preference == mood:
            return mood

        if any(
            word in preference
            for word in words
        ):
            return mood

    return None


def mood_match_score(preference, game):
    """Return mood relevance from 0 to 20."""

    preference = normalize_text(
        preference
    )

    if not preference:
        return 0

    mood_group = get_mood_group(
        preference
    )

    game_text = get_game_text(
        game
    )

    if mood_group:

        words = MOOD_WORDS[
            mood_group
        ]

        matches = sum(
            1
            for word in words
            if word in game_text
        )

        if matches >= 2:
            return 20

        if matches == 1:
            return 12

    # Generic natural-language mood matching

    tokens = tokenize(
        preference
    )

    game_tokens = tokenize(
        game_text
    )

    overlap = (
        tokens
        & game_tokens
    )

    if overlap:
        return min(
            10,
            len(overlap) * 4
        )

    return 0


def mood_match(preference, game):
    return (
        mood_match_score(
            preference,
            game
        ) > 0
    )


# ============================================================
# PLATFORM MATCHING
# ============================================================

PLATFORM_ALIASES = {

    "pc": {
        "pc",
        "microsoft windows",
        "windows",
    },

    "windows": {
        "pc",
        "microsoft windows",
        "windows",
    },

    "xbox": {
        "xbox",
        "xbox one",
        "xbox series x s",
        "xbox series",
    },

    "playstation": {
        "playstation",
        "playstation 4",
        "playstation 5",
        "ps4",
        "ps5",
    },

    "ps4": {
        "playstation 4",
        "ps4",
    },

    "ps5": {
        "playstation 5",
        "ps5",
    },

    "switch": {
        "nintendo switch",
        "switch",
    },

    "nintendo switch": {
        "nintendo switch",
        "switch",
    },

    "mobile": {
        "android",
        "ios",
        "mobile",
    },

    "android": {
        "android",
    },

    "ios": {
        "ios",
    },
}


def platform_match_score(preference, game):
    """Return platform relevance from -15 to 15."""

    preference = normalize_text(
        preference
    )

    if not preference:
        return 0

    if preference in {
        "any",
        "any platform",
        "all",
        "all platforms",
    }:
        return 0

    platforms = [
        normalize_text(
            platform.get("name", "")
        )
        for platform in game.get(
            "platforms",
            []
        )
    ]

    requested = PLATFORM_ALIASES.get(
        preference,
        {preference}
    )

    for platform in platforms:

        if platform in requested:
            return 15

        if (
            preference in platform
            or platform in preference
        ):
            return 15

    return -15


def platform_match(preference, game):
    return (
        platform_match_score(
            preference,
            game
        ) > 0
    )


# ============================================================
# DIFFICULTY
# ============================================================

def difficulty_score(preference, game):
    """Return difficulty relevance from 0 to 5."""

    preference = normalize_text(
        preference
    )

    if preference in {
        "",
        "any",
        "not specified",
    }:
        return 0

    text = get_game_text(
        game
    )

    if preference in {
        "hard",
        "challenging",
        "difficult",
        "hardcore",
    }:

        words = {
            "hard",
            "difficult",
            "challenging",
            "hardcore",
            "soulslike",
            "souls like",
            "punishing",
        }

        return 5 if any(
            word in text
            for word in words
        ) else 0

    if preference == "easy":

        words = {
            "easy",
            "casual",
            "relaxing",
            "accessible",
            "simple",
        }

        return 5 if any(
            word in text
            for word in words
        ) else 0

    return 0


def difficulty_match(preference, game):
    return (
        difficulty_score(
            preference,
            game
        ) > 0
    )


# ============================================================
# PLAYTIME
# ============================================================

def playtime_score(preference, game):
    """Return playtime relevance from 0 to 5."""

    preference = normalize_text(
        preference
    )

    if preference in {
        "",
        "any",
        "not specified",
    }:
        return 0

    text = get_game_text(
        game
    )

    if preference == "long":

        words = {
            "open world",
            "campaign",
            "hundreds",
            "hours",
            "extensive",
            "large adventure",
        }

        return 5 if any(
            word in text
            for word in words
        ) else 0

    if preference in {
        "short",
        "casual",
        "quick",
    }:

        words = {
            "short",
            "casual",
            "quick",
            "relaxing",
            "simple",
        }

        return 5 if any(
            word in text
            for word in words
        ) else 0

    return 0


def playtime_match(preference, game):
    return (
        playtime_score(
            preference,
            game
        ) > 0
    )


# ============================================================
# MULTIPLAYER
# ============================================================

def multiplayer_score(preference, game):
    """
    Return multiplayer relevance from 0 to 5.

    If the user explicitly wants multiplayer, games with
    multiplayer evidence receive a bonus.

    If the user explicitly wants single player, games with
    multiplayer-only language are slightly penalized.
    """

    text = get_game_text(
        game
    )

    multiplayer_words = {
        "multiplayer",
        "co op",
        "cooperative",
        "online multiplayer",
        "online",
    }

    has_multiplayer = any(
        word in text
        for word in multiplayer_words
    )

    if preference is True:
        return 5 if has_multiplayer else 0

    if preference is False:
        return 5 if not has_multiplayer else 0

    return 0


# ============================================================
# RATING
# ============================================================

def rating_score(game):
    """Return rating bonus from 0 to 5."""

    rating = game.get(
        "rating"
    )

    if rating is None:
        return 0

    try:
        rating = float(
            rating
        )
    except (
        TypeError,
        ValueError
    ):
        return 0

    if rating >= 85:
        return 5

    if rating >= 75:
        return 4

    if rating >= 65:
        return 3

    if rating >= 50:
        return 2

    return 0


# ============================================================
# DESCRIPTION RELEVANCE
# ============================================================

def description_score(
    preferences,
    game
):
    """
    Score description relevance from 0 to 20.
    """

    summary = normalize_text(
        game.get(
            "summary",
            ""
        )
    )

    if not summary:
        return 0

    score = 0

    genre = normalize_text(
        preferences.get(
            "genre",
            ""
        )
    )

    mood = normalize_text(
        preferences.get(
            "mood",
            ""
        )
    )

    # Genre evidence
    genre_group = get_genre_group(
        genre
    )

    if genre_group:

        synonyms = GENRE_SYNONYMS[
            genre_group
        ]

        if any(
            synonym in summary
            for synonym in synonyms
        ):
            score += 8

    else:

        tokens = tokenize(
            genre
        )

        summary_tokens = tokenize(
            summary
        )

        if tokens & summary_tokens:
            score += 8

    # Mood evidence
    mood_group = get_mood_group(
        mood
    )

    if mood_group:

        words = MOOD_WORDS[
            mood_group
        ]

        if any(
            word in summary
            for word in words
        ):
            score += 7

    # Difficulty
    score += min(
        3,
        difficulty_score(
            preferences.get(
                "difficulty",
                ""
            ),
            game
        )
    )

    # Playtime
    score += min(
        2,
        playtime_score(
            preferences.get(
                "playtime",
                ""
            ),
            game
        )
    )

    return min(
        score,
        20
    )


# ============================================================
# QUALITY PENALTY
# ============================================================

def genre_quality_penalty(
    preferences,
    game
):
    """
    Apply small penalties when evidence strongly suggests
    the game is dominated by an unrelated genre.

    These penalties are intentionally conservative.
    """

    genre = normalize_text(
        preferences.get(
            "genre",
            ""
        )
    )

    game_genres = [
        normalize_text(
            g.get(
                "name",
                ""
            )
        )
        for g in game.get(
            "genres",
            []
        )
    ]

    text = get_game_text(
        game
    )

    penalty = 0

    # RPG + clearly puzzle dominated
    if "rpg" in genre:

        if (
            "puzzle" in game_genres
            and (
                "jigsaw" in text
                or "puzzle game" in text
            )
        ):
            penalty += 15

    # Racing + clearly board/card dominated
    if "racing" in genre:

        if (
            "card" in text
            or "board game" in text
        ):
            penalty += 10

    # Farming + unrelated puzzle
    if (
        "farm" in genre
        or "farming" in genre
    ):

        if (
            "puzzle" in game_genres
            and "farm" not in text
            and "farming" not in text
        ):
            penalty += 10

    return penalty


# ============================================================
# MAIN SCORE
# ============================================================

def calculate_score(
    game,
    preferences
):
    """
    Calculate a match score from 0 to 100.

    The system deliberately avoids hard genre filtering.
    This makes the recommender robust to new or unusual
    genres and natural-language requests.
    """

    genre = preferences.get(
        "genre",
        ""
    )

    score = 0

    # --------------------------------------------------------
    # Genre: maximum 40
    # --------------------------------------------------------

    score += genre_match_score(
        genre,
        game
    )

    # --------------------------------------------------------
    # Mood: maximum 20
    # --------------------------------------------------------

    score += mood_match_score(
        preferences.get(
            "mood",
            ""
        ),
        game
    )

    # --------------------------------------------------------
    # Platform: +15 or -15
    # --------------------------------------------------------

    score += platform_match_score(
        preferences.get(
            "platform",
            ""
        ),
        game
    )

    # --------------------------------------------------------
    # Description: maximum 20
    # --------------------------------------------------------

    score += description_score(
        preferences,
        game
    )

    # --------------------------------------------------------
    # Rating: maximum 5
    # --------------------------------------------------------

    score += rating_score(
        game
    )

    # --------------------------------------------------------
    # Difficulty: maximum 5
    # --------------------------------------------------------

    score += difficulty_score(
        preferences.get(
            "difficulty",
            ""
        ),
        game
    )

    # --------------------------------------------------------
    # Playtime: maximum 5
    # --------------------------------------------------------

    score += playtime_score(
        preferences.get(
            "playtime",
            ""
        ),
        game
    )

    # --------------------------------------------------------
    # Multiplayer: maximum 5
    # --------------------------------------------------------

    score += multiplayer_score(
        preferences.get(
            "multiplayer"
        ),
        game
    )

    # --------------------------------------------------------
    # Quality penalty
    # --------------------------------------------------------

    score -= genre_quality_penalty(
        preferences,
        game
    )

    return max(
        0,
        min(
            round(score),
            100
        )
    )


# ============================================================
# RELEVANCE
# ============================================================

def is_relevant_game(
    game,
    preferences
):
    """
    Do NOT hard-filter based on genre.

    Any candidate with a usable score is retained.

    This is important because IGDB can return useful games
    for genres/subgenres that are not explicitly known to
    our local vocabulary.
    """

    return True


# ============================================================
# RANK GAMES
# ============================================================

def rank_games(
    games,
    preferences
):
    """
    Score every candidate and return them sorted by
    recommendation score.
    """

    ranked_games = []

    for game in games:

        if not is_relevant_game(
            game,
            preferences
        ):
            continue

        score = calculate_score(
            game,
            preferences
        )

        game_copy = game.copy()

        game_copy[
            "match_score"
        ] = score

        ranked_games.append(
            game_copy
        )

    ranked_games.sort(
        key=lambda game:
        game.get(
            "match_score",
            0
        ),
        reverse=True
    )

    return ranked_games