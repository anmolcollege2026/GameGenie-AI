# 🎮 GameGenie AI — Project Documentation

**AI-powered game discovery based on what you actually want to play.**

- **GitHub Repository:** https://github.com/Akshitcodes-code/GameGenie-AI
- **Working Demo:** https://gamegenie-ai-dz5jx5vgffkvpkdrdtkeek.streamlit.app/

---

## 1. Project Overview

GameGenie AI is an AI-powered game discovery and recommendation platform.

Instead of requiring users to search through game genres, platforms, ratings, themes, and other filters manually, GameGenie AI allows them to describe the kind of game they want using natural language.

For example:

> I want a dark challenging RPG for PC that I can play alone.

The system uses Google Gemini to understand the request, IGDB to discover candidate games, and a custom Python ranking engine to determine which candidates best match the user's preferences.

The final recommendations are presented through an interactive Streamlit web application.

---

## 2. Problem Statement

Game catalogs contain thousands of titles across many genres, platforms, themes, and play styles.

Traditional discovery often requires users to:

- Search by genre
- Check platform availability
- Compare ratings
- Read descriptions
- Consider multiplayer or single-player preferences
- Evaluate mood, difficulty, and play style
- Repeat the process across many games

This can make finding the right game time-consuming.

GameGenie AI addresses this problem by allowing the user to explain what they want naturally and then automatically converting that request into a ranked set of game recommendations.

---

## 3. Proposed Solution

GameGenie AI combines three main components:

1. **Natural-language understanding using Google Gemini**
2. **Game discovery using the IGDB API**
3. **Custom rule-based ranking using Python**

The AI does not simply choose a game and return it as the answer.

Instead, Gemini extracts structured preferences and search concepts. IGDB provides candidate games. GameGenie's Python ranking system evaluates those candidates and produces the final ranking.

This separation makes the recommendation process more transparent and controllable.

---

## 4. System Workflow

The application follows this pipeline:

```text
User Natural-Language Request
            ↓
      Google Gemini
            ↓
   Preference Extraction
            ↓
      Search Queries
            ↓
          IGDB
            ↓
     Candidate Games
            ↓
   Candidate Deduplication
            ↓
   Custom Python Ranking
            ↓
    Ranked Recommendations
            ↓
      Streamlit UI
```

### Step 1 — User Input

The user describes their desired gaming experience in natural language.

Example:

```text
I want a dark challenging RPG for PC that I can play alone.
```

### Step 2 — Preference Extraction

Google Gemini analyzes the request and extracts useful preference information such as:

- Genre
- Mood
- Platform
- Multiplayer preference
- Difficulty
- Playtime
- Search concepts

These preferences are then used to create search terms for game discovery.

### Step 3 — Candidate Discovery

The generated search terms are sent to IGDB.

GameGenie uses multiple search terms to increase candidate coverage rather than relying on only one query.

The retrieved games are combined and duplicate games are removed using their IGDB IDs.

### Step 4 — Ranking

The candidate games are passed into the custom Python ranking engine.

The ranking system evaluates how well each candidate matches the user's preferences.

### Step 5 — Recommendations

The highest-ranked games are displayed in the Streamlit interface.

Each recommendation can include:

- Game name
- Match score
- Description
- Genres
- Platforms
- IGDB rating
- Explanation of why the game matched

---

## 5. AI Integration — Google Gemini

Google Gemini is used for **understanding the user's request**, rather than directly deciding the final recommendation.

Its role is to transform an unstructured natural-language request into useful structured preferences and search concepts.

For example:

```text
User:
I want a dark challenging RPG for PC that I can play alone.
```

Conceptually, the application can derive preferences such as:

```text
Genre: RPG
Mood: Dark
Platform: PC
Multiplayer: Single Player
Difficulty: Challenging
```

The extracted information is then used by the rest of the recommendation pipeline.

This architecture keeps natural-language understanding separate from deterministic ranking.

---

## 6. Game Data — IGDB

GameGenie uses the **IGDB API** as its game information source.

IGDB provides information used during candidate discovery and ranking, including data such as:

- Game name
- Summary/description
- Genres
- Themes
- Game modes
- Platforms
- Ratings
- Release information
- Cover information when available

IGDB access uses Twitch OAuth authentication.

The application retrieves a Twitch access token and uses it when querying the IGDB API.

---

## 7. Candidate Search Strategy

A single natural-language search query may not discover enough relevant games.

GameGenie therefore expands the generated search terms.

The search process can use:

- Original Gemini-generated queries
- Important individual concepts
- Useful two-word combinations

Common low-value words are filtered to reduce noisy searches.

The resulting terms are deduplicated before querying IGDB.

Games are then deduplicated using their IGDB IDs.

This produces a larger and more diverse candidate pool for the ranking stage.

---

## 8. Ranking System

GameGenie uses a custom rule-based ranking engine.

The ranking logic is independent from Gemini.

Gemini understands the request.

The Python ranking engine makes the final recommendation decision.

### Ranking factors

| Factor | Purpose |
|---|---|
| Genre | Determines whether the game matches requested genres |
| Mood | Evaluates whether the game's themes and description fit the requested mood |
| Platform | Checks whether the game is available on the requested platform |
| Description | Measures relevance of useful preference keywords in the game description |
| IGDB Rating | Adds an external quality signal |

The resulting score is normalized to a maximum of:

```text
100
```

The games are then sorted by their final Match Score.

---

## 9. Explainable Recommendations

GameGenie is designed to provide more than a list of game names.

The interface presents a Match Score and an explanation of why a game matched the user's request.

This makes the recommendations easier to understand and gives the user visibility into the factors contributing to a recommendation.

---

## 10. User Interface

The frontend is built with Streamlit.

The interface provides:

- A natural-language input area
- Preference understanding
- Recommended games
- Match scores
- Game descriptions
- Genres
- Platforms
- IGDB ratings when available
- Match explanations

The application is publicly deployed and can be accessed here:

**Working Demo:**  
https://gamegenie-ai-dz5jx5vgffkvpkdrdtkeek.streamlit.app/

---

## 11. Technology Stack

### Frontend

- Streamlit

### Artificial Intelligence

- Google Gemini
- Google GenAI Python SDK

### Game Database

- IGDB API
- Twitch OAuth authentication

### Backend

- Python

### Supporting Libraries

- Requests
- Python-dotenv

---

## 12. Project Structure

```text
GameGenie-AI/
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── services/
│   ├── igdb_service.py
│   └── llm_parser.py
│
└── utils/
    └── ranking.py
```

### Main files

#### `app.py`

Runs the Streamlit application and connects the user interface to the recommendation pipeline.

#### `config.py`

Provides application configuration and environment-variable access.

#### `services/llm_parser.py`

Handles the Google Gemini integration and preference extraction.

#### `services/igdb_service.py`

Handles Twitch authentication and IGDB game searches.

#### `utils/ranking.py`

Contains the custom game-ranking logic.

#### `requirements.txt`

Contains the Python dependencies required to run the project.

#### `.env.example`

Provides the expected environment-variable structure without exposing real API credentials.

#### `.gitignore`

Prevents sensitive files and development artifacts such as `.env`, virtual environments, Python cache files, and editor settings from being committed.

---

## 13. Installation

### Prerequisites

- Python 3.x
- Google Gemini API key
- Twitch Client ID
- Twitch Client Secret

### Clone the repository

```bash
git clone https://github.com/Akshitcodes-code/GameGenie-AI.git
```

### Enter the project directory

```bash
cd GameGenie-AI
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate on Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Activate on Windows Command Prompt

```cmd
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 14. Environment Variables

Create a `.env` file in the project root.

```text
GEMINI_API_KEY=your_gemini_api_key
TWITCH_CLIENT_ID=your_twitch_client_id
TWITCH_CLIENT_SECRET=your_twitch_client_secret
```

Never commit the `.env` file to GitHub.

The repository's `.gitignore` excludes `.env`.

---

## 15. Running Locally

After installing the dependencies and configuring the environment variables:

```bash
streamlit run app.py
```

Streamlit will provide a local URL that can be opened in a browser.

---

## 16. Testing and Verification

The application was tested through the complete recommendation flow.

A representative test request is:

```text
I want a dark challenging RPG for PC that I can play alone.
```

The expected pipeline is:

```text
User request
     ↓
Gemini preference extraction
     ↓
Search query generation
     ↓
IGDB candidate discovery
     ↓
Duplicate removal
     ↓
Custom ranking
     ↓
Top recommendations
```

The working deployed application is available at:

https://gamegenie-ai-dz5jx5vgffkvpkdrdtkeek.streamlit.app/

---

## 17. Example

### User Input

```text
I want a dark challenging RPG for PC that I can play alone.
```

### GameGenie Understands

```text
Genre: RPG
Mood: Dark
Platform: PC
Multiplayer: Single Player
Difficulty: Challenging
```

### Example Recommendations

The application can produce ranked recommendations such as:

1. Bladebound
2. Hardcore Mecha
3. 5089: The Action RPG
4. Epic Battle Fantasy 4
5. Dark Fantasy: Jigsaw Puzzle

The exact recommendations and scores can change because the application queries live IGDB data and ranks the returned candidates dynamically.

---

## 18. Security

GameGenie AI keeps API credentials outside the source code.

Sensitive configuration is supplied through environment variables or Streamlit deployment secrets.

The repository excludes:

```text
.env
venv/
__pycache__/
*.pyc
.vscode/
```

No API keys should be placed directly into Python source files or committed to the public repository.

---

## 19. Advantages

### Natural Interaction

Users describe what they want in their own words instead of completing a large filter form.

### AI-Powered Understanding

Gemini converts natural-language descriptions into structured recommendation preferences.

### Broad Candidate Discovery

Multiple search terms are used to improve the candidate pool.

### Transparent Ranking

The final recommendation ranking is performed by custom Python logic rather than allowing the language model to arbitrarily choose the final result.

### Explainable Results

Users receive Match Scores and information explaining why games matched their preferences.

### Live Game Data

IGDB provides current game information for the discovery process.

---

## 20. Limitations

The current version has several practical limitations:

- Recommendation quality depends on the quality of the extracted preferences.
- IGDB search results determine the available candidate pool.
- Mood, difficulty, and playtime matching are based on available game information and the implemented ranking logic.
- Recommendations can change as live IGDB data changes.
- API availability and rate limits can affect the application.
- The current version does not include user accounts or long-term personalization.

---

## 21. Future Improvements

Possible future improvements include:

- 🎮 More advanced semantic game matching
- 🖼️ Game cover images
- 🔗 Direct links to game stores
- 👤 User accounts and saved recommendations
- ❤️ Favorite games
- 📊 Personalized recommendation history
- 🧠 More detailed preference extraction
- 🎯 Better difficulty and playtime matching
- 👥 Multiplayer and co-op filtering
- 📱 Improved mobile interface
- ⚡ Parallel IGDB searching
- 🔎 More advanced ranking and similarity algorithms
- 📈 Recommendation feedback and learning from user choices

---

## 22. Project Impact

GameGenie AI aims to reduce the friction involved in discovering games.

Instead of asking users to know exactly which genre, tag, platform, rating, or filter to select, it lets them explain their desired experience naturally.

The project demonstrates how generative AI can be combined with external APIs and deterministic recommendation logic to create a practical, explainable AI-powered application.

---

## 23. Project Links

### 💻 GitHub Repository

https://github.com/Akshitcodes-code/GameGenie-AI

### 🌐 Working Demo

https://gamegenie-ai-dz5jx5vgffkvpkdrdtkeek.streamlit.app/

### 📄 Project Documentation

This document.

### ▶️ YouTube Explanation Video

To be added after the project explanation video is recorded.

---

## 24. Hackathon Context

GameGenie AI was developed as a hackathon project focused on improving personalized game discovery using artificial intelligence.

The project demonstrates the integration of:

- Generative AI
- Natural-language processing
- External APIs
- Game data retrieval
- Recommendation algorithms
- Rule-based ranking
- Explainable recommendations
- Interactive web applications
- Cloud deployment

---

## 25. Conclusion

GameGenie AI combines natural-language understanding, live game data, and custom recommendation logic into a single game discovery experience.

The system's core idea is simple:

```text
Tell GameGenie what you want to play.
            ↓
AI understands your preferences.
            ↓
IGDB finds possible games.
            ↓
GameGenie ranks the candidates.
            ↓
You get personalized recommendations.
```

The project is publicly available on GitHub and has a working Streamlit deployment.

**GameGenie AI — Find the game that fits what you actually want to play.**
