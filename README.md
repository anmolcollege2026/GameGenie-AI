# 🎮 GameGenie AI

AI-powered game discovery based on what you actually want to play.

GameGenie AI is an AI-powered game recommendation platform that allows users to describe the type of game they want using natural language.

Instead of manually searching through hundreds of games, users can simply describe their preferences, such as genre, mood, platform, difficulty, multiplayer preference, and playtime.

GameGenie AI uses Google Gemini to understand the user's request, IGDB to discover candidate games, and a custom Python ranking engine to determine the best matches.

---

## 🚀 Features

- 🎮 Natural-language game discovery
- 🧠 Google Gemini preference extraction
- 🔎 IGDB game database search
- 🔍 Multiple search queries for better candidate discovery
- 🏆 Custom Python game ranking
- 🎯 Genre matching
- 🌙 Mood matching
- 🖥️ Platform matching
- 📝 Game description relevance scoring
- ⭐ IGDB rating integration
- 💡 Explanation of why a game matched
- 🌐 Interactive Streamlit web interface
- 🔐 API keys stored using environment variables

---

## 🧠 How GameGenie AI Works

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
   Custom Python Ranking
            ↓
    Ranked Recommendations
            ↓
      Streamlit UI
Step 1 — Understand the User

The user describes the type of game they want.

Example:

I want a dark challenging RPG for PC that I can play alone.

Google Gemini extracts structured preferences such as:

Genre
Mood
Platform
Multiplayer preference
Difficulty
Playtime
Search queries
Step 2 — Search IGDB

The generated search queries are sent to IGDB.

Multiple search queries are used to discover a larger and more diverse set of candidate games.

Duplicate games are removed using their IGDB IDs.

Step 3 — Rank the Games

The candidate games are passed through GameGenie's custom Python ranking engine.

The ranking engine evaluates:

Genre compatibility
Mood compatibility
Platform compatibility
Description relevance
IGDB rating

Each game receives a final Match Score from:

0–100
Step 4 — Display Recommendations

The highest-ranked games are displayed in the Streamlit interface.

Each recommendation includes:

Game name
Match score
Description
Genres
Platforms
IGDB rating
Explanation of why the game matched
🏆 Ranking System

GameGenie AI uses a custom rule-based ranking engine.

The ranking logic is implemented independently from Gemini.

Gemini is responsible for understanding the user's request and extracting preferences.

The final recommendation decision is made by GameGenie's Python ranking system.

Ranking Factors
Factor	Purpose
Genre	Determines whether the game belongs to the requested genre
Mood	Checks whether the game's description and themes match the requested mood
Platform	Checks whether the game is available on the requested platform
Description	Measures relevance of important keywords in the game's description
IGDB Rating	Provides an additional quality signal

The resulting score is normalized to a maximum of:

100
🛠️ Technology Stack
Frontend
Streamlit
AI
Google Gemini
Google GenAI Python SDK
Game Database
IGDB API
Twitch OAuth authentication
Backend
Python
Supporting Libraries
Requests
Python-dotenv
📁 Project Structure
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
⚙️ Installation
1. Clone the repository
git clone https://github.com/Akshitcodes-code/GameGenie-AI.git
2. Enter the project directory
cd GameGenie-AI
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment
Windows PowerShell
.\venv\Scripts\Activate.ps1
Windows Command Prompt
venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
🔑 Environment Variables

GameGenie AI requires API credentials for Google Gemini and IGDB/Twitch.

Create a .env file in the project root.

GEMINI_API_KEY=your_gemini_api_key
TWITCH_CLIENT_ID=your_twitch_client_id
TWITCH_CLIENT_SECRET=your_twitch_client_secret

Never commit the .env file to GitHub.

The .gitignore file is configured to prevent API keys from being uploaded.

▶️ Running the Application

After installing the dependencies and configuring the environment variables, run:

streamlit run app.py

The application will start locally and provide a URL that can be opened in a web browser.

🧪 Testing

The ranking engine and Gemini preference extraction can be tested locally using the project's test scripts.

Example:

python test_ranking.py

The application should:

Extract the user's preferences.
Generate search queries.
Search IGDB.
Find candidate games.
Rank the candidates.
Display the highest-scoring games.
💡 Example
User Input
I want a dark challenging RPG for PC that I can play alone.
GameGenie Understands
Genre: RPG
Mood: Dark
Platform: PC
Multiplayer: Single Player
Difficulty: Challenging
Playtime: Long
Example Recommendations
1. Bladebound
2. Hardcore Mecha
3. 5089: The Action RPG
4. Epic Battle Fantasy 4
5. Dark Fantasy: Jigsaw Puzzle

The exact recommendations and scores depend on the current IGDB results.

🎯 Project Objective

The goal of GameGenie AI is to make game discovery easier and more personalized.

Traditional game discovery often requires users to manually search through genres, ratings, platforms, reviews, and large game catalogs.

GameGenie AI simplifies this process by allowing users to describe what they want naturally.

The system combines:

Natural Language Understanding
            +
Game Database Search
            +
Custom Recommendation Logic

to produce personalized game recommendations.

🌟 Why GameGenie AI?
Natural Interaction

Users can describe what they want instead of selecting dozens of filters.

AI-Powered Understanding

Google Gemini converts natural-language requests into structured preferences.

Data-Driven Discovery

IGDB provides game information including genres, platforms, themes, descriptions, and ratings.

Transparent Recommendations

The ranking is performed using custom Python logic instead of allowing the AI model to arbitrarily choose the final result.

Explainable Results

GameGenie shows users why a particular game matched their request.

🔮 Future Improvements

Possible future improvements include:

🎮 More advanced semantic game matching
🖼️ Game cover images
🔗 Direct links to game stores
👤 User accounts and saved recommendations
❤️ Favorite games
📊 Personalized recommendation history
🧠 More detailed preference extraction
🎯 Better difficulty and playtime matching
👥 Multiplayer and co-op filtering
📱 Improved mobile interface
⚡ Faster parallel IGDB searching
🔎 More advanced ranking and similarity algorithms
🔐 Security

API credentials are stored in environment variables rather than directly inside the source code.

The following files and directories are excluded from Git:

.env
venv/
__pycache__/
*.pyc
.vscode/

Users should create their own .env file when running the project locally.

📌 Project Links
💻 GitHub Repository

https://github.com/Akshitcodes-code/GameGenie-AI

🌐 Working Demo

To be added after deployment.

📄 Project Documentation

To be added.

▶️ YouTube Explanation Video

To be added.

🏁 Hackathon Project

GameGenie AI was developed as a hackathon project focused on using AI to improve personalized game discovery.

The project demonstrates the integration of:

Generative AI
External APIs
Natural-language processing
Recommendation algorithms
Rule-based ranking
Interactive web applications
📜 License

This project is created for educational and hackathon purposes.


### Then save it.

**Do NOT add anything else to `README.md`.**

Then, in PowerShell, run only these commands:

```powershell
git status