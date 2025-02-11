import os
import httpx
from http import HTTPStatus

from dotenv import load_dotenv
from fastapi import HTTPException

from what_to_wear.api.models.current_weather import CurrentWeather

load_dotenv()

weather_api_base_url = os.getenv("WEATHER_API_BASE_URL")
weather_api_key = os.getenv("WEATHER_API_KEY")


async def get_current_weather_data(lat: str, lon: str) -> CurrentWeather:
    try:

        q_param = f"{lat},{lon}"

        print(weather_api_base_url)

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{weather_api_base_url}/current.json",
                params={"key": weather_api_key, "q": q_param},
                timeout=10.0
                )
            response.raise_for_status()

            return response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Weather API error")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Service unavailable")
    except Exception as e:
        HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"{e}")
