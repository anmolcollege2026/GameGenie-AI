import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
RAWG_API_KEY = os.getenv("RAWG_API_KEY")