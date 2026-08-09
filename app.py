import streamlit as st

from services.llm_parser import extract_preferences
from services.igdb_service import search_multiple_terms
from utils.ranking import (
    rank_games,
    genre_match,
    mood_match,
    platform_match
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="GameGenie AI",
    page_icon="🎮",
    layout="wide"
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.2rem;
        opacity: 0.75;
        margin-bottom: 2rem;
    }

    .section-title {
        font-size: 1.7rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    .game-description {
        line-height: 1.6;
        opacity: 0.9;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎮 GameGenie AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered game discovery based on what you actually want to play.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# USER INPUT
# ============================================================

st.markdown(
    '<div class="section-title">🔎 What do you want to play?</div>',
    unsafe_allow_html=True
)

user_prompt = st.text_area(
    "Describe your ideal game",
    placeholder=(
        "Example: I want a relaxing farming game "
        "that I can play alone on PC."
    ),
    height=130,
    label_visibility="collapsed"
)


# ============================================================
# SEARCH BUTTON
# ============================================================

search_clicked = st.button(
    "🔎 Find My Games",
    type="primary",
    use_container_width=True
)


if search_clicked:

    # ========================================================
    # VALIDATE INPUT
    # ========================================================

    if not user_prompt.strip():

        st.warning(
            "Please describe the game you want."
        )

    else:

        # ====================================================
        # STEP 1 — GEMINI
        # ====================================================

        with st.spinner(
            "🧠 Understanding your preferences..."
        ):

            preferences = extract_preferences(
                user_prompt
            )

        st.success(
            "Preferences understood!"
        )

        with st.expander(
            "🧠 See what GameGenie understood"
        ):

            st.json(preferences)


        # ====================================================
        # STEP 2 — SEARCH IGDB
        # ====================================================

        search_queries = preferences.get(
            "search_queries",
            []
        )

        with st.spinner(
            "🎮 Searching game database..."
        ):

            games = search_multiple_terms(
                search_queries,
                limit_per_term=10
            )


        # ====================================================
        # NO RESULTS
        # ====================================================

        if not games:

            st.warning(
                "We couldn't find any games. "
                "Try describing your request differently."
            )


        else:

            # =================================================
            # STEP 3 — RANK GAMES
            # =================================================

            with st.spinner(
                "⚡ Finding the best matches..."
            ):

                ranked_games = rank_games(
                    games,
                    preferences
                )


            # =================================================
            # RESULTS HEADER
            # =================================================

            st.markdown(
                '<div class="section-title">'
                '🏆 Recommended Games'
                '</div>',
                unsafe_allow_html=True
            )

            st.caption(
                f"Found {len(games)} candidate games • "
                f"Showing the top {min(5, len(ranked_games))}"
            )


            # =================================================
            # GAME RESULTS
            # =================================================

            for index, game in enumerate(
                ranked_games[:5],
                start=1
            ):

                # ---------------------------------------------
                # BASIC GAME INFORMATION
                # ---------------------------------------------

                name = game.get(
                    "name",
                    "Unknown Game"
                )

                score = game.get(
                    "match_score",
                    0
                )

                rating = game.get(
                    "rating"
                )

                summary = game.get(
                    "summary",
                    "No description available."
                )

                genres = game.get(
                    "genres",
                    []
                )

                platforms = game.get(
                    "platforms",
                    []
                )


                # ---------------------------------------------
                # COVER IMAGE
                # ---------------------------------------------

                cover = game.get(
                    "cover",
                    {}
                )

                cover_url = None

                if isinstance(cover, dict):

                    cover_url = cover.get(
                        "url"
                    )

                    # IGDB sometimes returns URLs
                    # without the https:// prefix.
                    if cover_url and cover_url.startswith("//"):

                        cover_url = (
                            "https:"
                            + cover_url
                        )


                # ---------------------------------------------
                # GENRE NAMES
                # ---------------------------------------------

                genre_names = [
                    genre.get("name", "")
                    for genre in genres
                    if genre.get("name")
                ]


                # ---------------------------------------------
                # PLATFORM NAMES
                # ---------------------------------------------

                platform_names = [
                    platform.get("name", "")
                    for platform in platforms
                    if platform.get("name")
                ]


                # =================================================
                # GAME CARD
                # =================================================

                with st.container(
                    border=True
                ):

                    # ---------------------------------------------
                    # THREE COLUMN LAYOUT
                    # ---------------------------------------------

                    col1, col2, col3 = st.columns(
                        [1, 4, 1]
                    )


                    # ---------------------------------------------
                    # COVER
                    # ---------------------------------------------

                    with col1:

                        if cover_url:

                            try:

                                st.image(
                                    cover_url,
                                    use_container_width=True
                                )

                            except Exception:

                                st.write(
                                    "🎮"
                                )

                        else:

                            st.write(
                                "🎮"
                            )


                    # ---------------------------------------------
                    # TITLE + DESCRIPTION
                    # ---------------------------------------------

                    with col2:

                        st.markdown(
                            f"### 🎮 {index}. {name}"
                        )

                        st.markdown(
                            f'<div class="game-description">'
                            f'{summary}'
                            f'</div>',
                            unsafe_allow_html=True
                        )


                    # ---------------------------------------------
                    # MATCH SCORE
                    # ---------------------------------------------

                    with col3:

                        st.metric(
                            "Match",
                            f"{score}/100"
                        )


                    # =================================================
                    # GAME DETAILS
                    # =================================================

                    if genre_names:

                        st.write(
                            "🎯 **Genres:** "
                            + ", ".join(
                                genre_names
                            )
                        )


                    if platform_names:

                        st.write(
                            "🖥️ **Platforms:** "
                            + ", ".join(
                                platform_names
                            )
                        )


                    if rating is not None:

                        st.write(
                            f"⭐ **IGDB Rating:** "
                            f"{rating:.1f}/100"
                        )


                    # =================================================
                    # WHY THIS GAME MATCHED
                    # =================================================

                    matched = []


                    # ---------------------------------------------
                    # GENRE MATCH
                    # ---------------------------------------------

                    if preferences.get("genre"):

                        if genre_match(
                            preferences["genre"],
                            game
                        ):

                            matched.append(
                                f"Genre: "
                                f"{preferences['genre']}"
                            )


                    # ---------------------------------------------
                    # MOOD MATCH
                    # ---------------------------------------------

                    if preferences.get("mood"):

                        if mood_match(
                            preferences["mood"],
                            game
                        ):

                            matched.append(
                                f"Mood: "
                                f"{preferences['mood']}"
                            )


                    # ---------------------------------------------
                    # PLATFORM MATCH
                    # ---------------------------------------------

                    if preferences.get("platform"):

                        if platform_match(
                            preferences["platform"],
                            game
                        ):

                            matched.append(
                                f"Platform: "
                                f"{preferences['platform']}"
                            )


                    # ---------------------------------------------
                    # DISPLAY MATCH REASONS
                    # ---------------------------------------------

                    if matched:

                        with st.expander(
                            "💡 Why this game matched"
                        ):

                            for reason in matched:

                                st.write(
                                    f"✓ {reason}"
                                )