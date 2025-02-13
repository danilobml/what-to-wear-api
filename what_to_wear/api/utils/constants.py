import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

# Env variables:
WEATHER_API_BASE_URL = os.getenv("WEATHER_API_BASE_URL")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

LLM_API_URL = os.getenv("LLM_API_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
HEADERS = {"Authorization": f"Bearer {LLM_API_KEY}"}

DATABASE_URL = os.getenv("DATABASE_URL")


# Enums and other constants:
class RequestTypeEnum(str, Enum):
    CURRENT = "CURRENT"
    FORECAST = "FORECAST"


class ModelTypeEnum(str, Enum):
    MISTRAL = "MISTRAL"


# Change model here:
MODEL_TYPE = ModelTypeEnum.MISTRAL

MODEL_URLS = {
    ModelTypeEnum.MISTRAL: "mistralai/mistral-7b-instruct"
}


# Custom exceptions:
class NoModelSelectedException(Exception):
    """Exception raised when no valid model type is selected."""
    def __init__(self):
        super().__init__("No valid model type selected")


class MissingDataException(Exception):
    """ Exception caused when data that is essential for processing the request is missing """
