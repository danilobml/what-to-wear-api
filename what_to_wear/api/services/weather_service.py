import httpx
from http import HTTPStatus

from fastapi import HTTPException

from what_to_wear.api.models.current_weather import WeatherResponse
from what_to_wear.utils.constants import WEATHER_API_BASE_URL, WEATHER_API_KEY


async def get_current_weather_data(lat: str, lon: str) -> WeatherResponse:
    try:

        q_param = f"{lat},{lon}"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{WEATHER_API_BASE_URL}/current.json",
                params={"key": WEATHER_API_KEY, "q": q_param},
                timeout=10.0
                )
            response.raise_for_status()
            weather_dict = response.json()

            return WeatherResponse(**weather_dict)

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Weather API error")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Service unavailable")
    except Exception as e:
        HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"{e}")
