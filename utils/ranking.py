"""
GameGenie AI
Generic Game Ranking Engine

Gemini extracts the user's preferences.
This module independently scores and ranks games.
"""

# ============================================================
# GENRE GROUPS
# ============================================================

GENRE_GROUPS = {
    "farming": {
        "farming",
        "farm",
        "farming simulation",
        "farm simulation",
        "agriculture",
        "agricultural",
        "simulator",
    },

    "rpg": {
        "rpg",
        "role-playing",
        "role-playing (rpg)",
        "role playing",
    },

    "action": {
        "action",
        "shooter",
        "fighting",
        "hack and slash",
        "beat 'em up",
    },

    "adventure": {
        "adventure",
        "action-adventure",
    },

    "puzzle": {
        "puzzle",
    },

    "strategy": {
        "strategy",
        "tactical",
        "turn-based strategy",
    },

    "sports": {
        "sport",
        "sports",
    },

    "racing": {
        "racing",
        "driving",
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
    },

    "dark": {
        "dark",
        "horror",
        "survival",
        "thriller",
        "scary",
        "grim",
        "gloomy",
    },

    "challenging": {
        "hard",
        "difficult",
        "challenging",
        "souls-like",
        "soulslike",
        "hardcore",
    },
}


# ============================================================
# TEXT HELPERS
# ============================================================

def normalize_text(text):
    """Convert text to lowercase normalized text."""

    if not text:
        return ""

    return str(text).lower().strip()


def get_game_text(game):
    """Combine useful searchable information about a game."""

    name = game.get("name", "")
    summary = game.get("summary", "")

    genres = " ".join(
        genre.get("name", "")
        for genre in game.get("genres", [])
    )

    themes = " ".join(
        theme.get("name", "")
        for theme in game.get("themes", [])
    )

    return normalize_text(
        f"{name} {summary} {genres} {themes}"
    )


# ============================================================
# GENRE HELPERS
# ============================================================

def get_genre_group(preference):
    """Find the conceptual genre group for a preference."""

    preference = normalize_text(preference)

    if not preference:
        return None

    for group_name, values in GENRE_GROUPS.items():

        if preference in values:
            return group_name

        for value in values:

            if value in preference:
                return group_name

            if preference in value:
                return group_name

    return None


def genre_match(preference, game):
    """Determine whether a game belongs to the requested genre."""

    preference = normalize_text(preference)

    if not preference:
        return False

    game_genres = [
        normalize_text(
            genre.get("name", "")
        )
        for genre in game.get("genres", [])
    ]

    # --------------------------------------------------------
    # Direct match
    # --------------------------------------------------------

    for genre in game_genres:

        if preference == genre:
            return True

        if preference in genre:
            return True

        if genre in preference:
            return True

    # --------------------------------------------------------
    # Concept-group match
    # --------------------------------------------------------

    requested_group = get_genre_group(preference)

    if requested_group:

        group_values = GENRE_GROUPS[
            requested_group
        ]

        for game_genre in game_genres:

            if game_genre in group_values:
                return True

            for value in group_values:

                if value in game_genre:
                    return True

    # --------------------------------------------------------
    # Farming text detection
    # --------------------------------------------------------

    if requested_group == "farming":

        farming_words = {
            "farm",
            "farming",
            "farmer",
            "agriculture",
            "agricultural",
            "crop",
            "crops",
            "harvest",
            "planting",
            "livestock",
            "cattle",
            "pasture",
        }

        game_text = get_game_text(game)

        if any(
            word in game_text
            for word in farming_words
        ):
            return True

    return False


# ============================================================
# MOOD MATCHING
# ============================================================

def get_mood_group(preference):
    """Return the requested mood group."""

    preference = normalize_text(preference)

    if not preference:
        return None

    for mood_name, words in MOOD_WORDS.items():

        if preference == mood_name:
            return mood_name

        if any(
            word in preference
            for word in words
        ):
            return mood_name

    return None


def mood_match(preference, game):
    """Determine whether the game contains evidence of the mood."""

    mood_group = get_mood_group(preference)

    if not mood_group:
        return False

    words = MOOD_WORDS[mood_group]

    name = normalize_text(
        game.get("name", "")
    )

    summary = normalize_text(
        game.get("summary", "")
    )

    themes = " ".join(
        normalize_text(
            theme.get("name", "")
        )
        for theme in game.get("themes", [])
    )

    # Strong evidence: description
    if any(word in summary for word in words):
        return True

    # Strong evidence: IGDB themes
    if any(word in themes for word in words):
        return True

    # Title alone is weak evidence.
    # We still allow it, but it should not be enough
    # to make a game look like a perfect match.
    return False

# ============================================================
# PLATFORM MATCHING
# ============================================================

def platform_match(preference, game):
    """Determine whether the requested platform is supported."""

    preference = normalize_text(preference)

    if not preference:
        return False

    platforms = [
        normalize_text(
            platform.get("name", "")
        )
        for platform in game.get(
            "platforms",
            []
        )
    ]

    # Common platform aliases
    aliases = {
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
            "xbox series x|s",
        },

        "playstation": {
            "playstation",
            "playstation 4",
            "playstation 5",
            "ps4",
            "ps5",
        },
    }

    requested_platforms = aliases.get(
        preference,
        {preference}
    )

    for platform in platforms:

        if platform in requested_platforms:
            return True

        if preference in platform:
            return True

        if platform in preference:
            return True

    return False


# ============================================================
# DIFFICULTY MATCHING
# ============================================================

def difficulty_match(preference, game):
    """Estimate difficulty relevance from game text."""

    preference = normalize_text(preference)

    if not preference:
        return False

    game_text = get_game_text(game)

    difficult_words = {
        "hard",
        "difficult",
        "challenging",
        "hardcore",
        "souls-like",
        "soulslike",
    }

    easy_words = {
        "easy",
        "casual",
        "relaxing",
        "cozy",
        "simple",
    }

    if (
        "challenging" in preference
        or "hard" in preference
    ):

        return any(
            word in game_text
            for word in difficult_words
        )

    if "easy" in preference:

        return any(
            word in game_text
            for word in easy_words
        )

    return False


# ============================================================
# PLAYTIME MATCHING
# ============================================================

def playtime_match(preference, game):
    """Estimate playtime relevance from game text."""

    preference = normalize_text(preference)

    if not preference:
        return False

    game_text = get_game_text(game)

    if "long" in preference:

        words = {
            "open world",
            "campaign",
            "hundreds",
            "hours",
            "adventure",
            "rpg",
        }

    elif (
        "casual" in preference
        or "short" in preference
        or "flexible" in preference
    ):

        words = {
            "casual",
            "relaxing",
            "cozy",
            "short",
            "quick",
            "simple",
        }

    else:
        return False

    return any(
        word in game_text
        for word in words
    )


# ============================================================
# RATING SCORE
# ============================================================

def rating_score(game):
    """Small bonus for highly rated games."""

    rating = game.get("rating")

    if rating is None:
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

def description_score(preferences, game):
    """Score textual relevance to the user's request."""

    summary = normalize_text(
        game.get("summary", "")
    )

    if not summary:
        return 0

    score = 0

    genre = normalize_text(
        preferences.get("genre", "")
    )

    mood = normalize_text(
        preferences.get("mood", "")
    )

    # --------------------------------------------------------
    # Genre vocabulary
    # --------------------------------------------------------

    genre_group = get_genre_group(genre)

    if genre_group:

        genre_words = GENRE_GROUPS[
            genre_group
        ]

        if any(
            word in summary
            for word in genre_words
        ):
            score += 8

    # --------------------------------------------------------
    # Mood vocabulary
    # --------------------------------------------------------

    mood_group = get_mood_group(mood)

    if mood_group:

        mood_words = MOOD_WORDS[
            mood_group
        ]

        if any(
            word in summary
            for word in mood_words
        ):
            score += 7

    # --------------------------------------------------------
    # Difficulty
    # --------------------------------------------------------

    difficulty = preferences.get(
        "difficulty",
        ""
    )

    if difficulty_match(
        difficulty,
        game
    ):
        score += 3

    # --------------------------------------------------------
    # Playtime
    # --------------------------------------------------------

    playtime = preferences.get(
        "playtime",
        ""
    )

    if playtime_match(
        playtime,
        game
    ):
        score += 2

    return min(score, 20)


# ============================================================
# RELEVANCE FILTER
# ============================================================

def is_relevant_game(game, preferences):
    """
    Remove games that are clearly unrelated
    to the requested genre.
    """

    genre = normalize_text(
        preferences.get("genre", "")
    )

    if not genre:
        return True

    return genre_match(
        genre,
        game
    )
def genre_quality_penalty(preferences, game):
    """
    Penalize games that technically match the requested genre
    but are dominated by a clearly different genre.
    """

    genre = normalize_text(
        preferences.get("genre", "")
    )

    game_genres = [
        normalize_text(
            g.get("name", "")
        )
        for g in game.get("genres", [])
    ]

    game_text = get_game_text(game)

    penalty = 0

    # --------------------------------------------------------
    # RPG requests
    # --------------------------------------------------------

    if "rpg" in genre:

        puzzle_evidence = (
            "puzzle" in game_genres
            or "jigsaw" in game_text
        )

        if puzzle_evidence:

            # If the game description is clearly about
            # puzzles/jigsaws, it is probably not a strong
            # RPG recommendation even if IGDB tags it RPG.
            if (
                "puzzle" in game_text
                or "jigsaw" in game_text
            ):
                penalty += 20

    # --------------------------------------------------------
    # Racing requests
    # --------------------------------------------------------

    if "racing" in genre:

        if (
            "puzzle" in game_genres
            or "card & board game" in game_genres
        ):
            penalty += 15

    # --------------------------------------------------------
    # Farming requests
    # --------------------------------------------------------

    if (
        "farm" in genre
        or "farming" in genre
    ):

        if (
            "puzzle" in game_genres
            and "farm" not in game_text
        ):
            penalty += 20

    return penalty

def preference_detail_score(preferences, game):
    """
    Score additional preferences such as difficulty,
    playtime, and multiplayer.
    """

    score = 0

    text = get_game_text(game)

    # -----------------------------------------
    # Difficulty
    # -----------------------------------------

    difficulty = normalize_text(
        preferences.get("difficulty", "")
    )

    if difficulty == "challenging":

        challenging_words = [
            "challenging",
            "difficult",
            "hard",
            "hardcore",
            "souls-like",
            "soulslike"
        ]

        if any(
            word in text
            for word in challenging_words
        ):
            score += 5

    elif difficulty == "easy":

        easy_words = [
            "easy",
            "casual",
            "relaxing",
            "accessible"
        ]

        if any(
            word in text
            for word in easy_words
        ):
            score += 5

    # -----------------------------------------
    # Playtime
    # -----------------------------------------

    playtime = normalize_text(
        preferences.get("playtime", "")
    )

    if playtime == "long":

        long_words = [
            "long",
            "extensive",
            "hundreds of hours",
            "open world",
            "campaign",
            "large adventure"
        ]

        if any(
            word in text
            for word in long_words
        ):
            score += 5

    elif playtime == "casual":

        casual_words = [
            "casual",
            "short",
            "quick",
            "relaxing"
        ]

        if any(
            word in text
            for word in casual_words
        ):
            score += 5

    # -----------------------------------------
    # Multiplayer
    # -----------------------------------------

    multiplayer = preferences.get(
        "multiplayer"
    )

    if multiplayer is False:

        multiplayer_words = [
            "multiplayer",
            "co-op",
            "cooperative",
            "online multiplayer"
        ]

        if not any(
            word in text
            for word in multiplayer_words
        ):
            score += 5

    return score
# ============================================================
# MAIN SCORING
# ============================================================

def calculate_score(game, preferences):
    """
    Calculate a match score from 0 to 100.

    Weighting:

    Genre       = 40
    Mood        = 20
    Platform    = 15
    Description = 20
    Rating      = 5
    """

    # --------------------------------------------------------
    # Genre
    # --------------------------------------------------------

    if not genre_match(
        preferences.get("genre", ""),
        game
    ):
        return 0

    score = 40

    # --------------------------------------------------------
    # Mood
    # --------------------------------------------------------

    mood_preference = preferences.get(
        "mood",
        ""
    )

    if mood_preference:

        if mood_match(
            mood_preference,
            game
        ):
            score += 20

    # --------------------------------------------------------
    # Platform
    # --------------------------------------------------------

    platform_preference = preferences.get(
        "platform",
        ""
    )

    if platform_preference:

        if platform_match(
            platform_preference,
            game
        ):
            score += 15

        else:
            # Strong penalty when user explicitly
            # requests a platform.
            score -= 15

    # --------------------------------------------------------
    # Description
    # --------------------------------------------------------

    score += description_score(
        preferences,
        game
    )

    # -------------------------------------
    # Rating
    # -------------------------------------

    score += rating_score(
        game
    )

    # -------------------------------------
    # Additional preferences
    # -------------------------------------

    score += preference_detail_score(
        preferences,
        game
    )

    # -------------------------------------
    # Genre quality penalty
    # -------------------------------------

    score -= genre_quality_penalty(
        preferences,
        game
    )

    return max(
        0,
        min(score, 100)
    )
# ============================================================
# RANK GAMES
# ============================================================

def rank_games(games, preferences):
    """Filter, score and sort games."""

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

        game_copy["match_score"] = score

        ranked_games.append(
            game_copy
        )

    ranked_games.sort(
        key=lambda game:
        game["match_score"],
        reverse=True
    )

    return ranked_games