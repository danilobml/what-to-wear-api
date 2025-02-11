import os

from dotenv import load_dotenv

load_dotenv()


WEATHER_API_BASE_URL = os.getenv("WEATHER_API_BASE_URL")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

LLM_API_URL = os.getenv("LLM_API_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
HEADERS = {"Authorization": f"Bearer {LLM_API_KEY}"}
