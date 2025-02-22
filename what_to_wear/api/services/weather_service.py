import httpx

from http import HTTPStatus
from fastapi import HTTPException

from what_to_wear.api.models.schemas.current_weather import CurrentWeatherResponse
from what_to_wear.api.models.schemas.forecast_weather import ForecastWeatherResponse
from what_to_wear.api.utils.constants import WEATHER_API_BASE_URL, WEATHER_API_KEY


async def get_current_weather_data(lat: str, lon: str) -> CurrentWeatherResponse:
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

            return CurrentWeatherResponse(**weather_dict)

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Weather API error")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Service unavailable")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


async def get_forecast_weather_data(lat: str, lon: str, days: int) -> ForecastWeatherResponse:
    try:
        q_param = f"{lat},{lon}"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{WEATHER_API_BASE_URL}/forecast.json",
                params={"key": WEATHER_API_KEY, "q": q_param, "days": days},
                timeout=10.0
            )
            response.raise_for_status()
            weather_dict = response.json()

            return ForecastWeatherResponse(**weather_dict)

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Weather API error")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Service unavailable")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
