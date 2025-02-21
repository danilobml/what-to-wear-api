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

SECRET_KEY = os.getenv("SECRET_KEY")


# Enums and other constants:
class RequestTypeEnum(str, Enum):
    CURRENT = "CURRENT"
    FORECAST = "FORECAST"


class ModelTypeEnum(str, Enum):
    MISTRAL = "MISTRAL"


# Auth:
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Change model here:
MODEL_TYPE = ModelTypeEnum.MISTRAL

MODEL_PARAMS = {
    ModelTypeEnum.MISTRAL: "mistralai/mistral-7b-instruct"
}


# CORS:
ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]


# Custom exceptions:
class NoModelSelectedException(Exception):
    """Exception raised when no valid model type is selected."""
    def __init__(self):
        super().__init__("No valid model type selected")


class MissingDataException(Exception):
    """ Exception caused when data that is essential for processing the request is missing """


class FailureCreatingUserException(Exception):
    """Exception raised when there is an error creating a new user."""
    def __init__(self):
        super().__init__("Failure creating user")


class UsernameAlreadyExistsException(Exception):
    """Exception raised when creating a new user with an already existing username """
    def __init__(self):
        super().__init__("Username already exists")
