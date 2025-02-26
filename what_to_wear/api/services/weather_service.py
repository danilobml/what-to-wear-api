from http import HTTPStatus
from typing import Optional

import httpx
from fastapi import HTTPException

from what_to_wear.api.models.schemas.current_weather import CurrentWeatherResponse
from what_to_wear.api.models.schemas.forecast_weather import ForecastWeatherResponse
from what_to_wear.api.utils.constants import WEATHER_API_BASE_URL, WEATHER_API_KEY


async def get_current_weather_data(
    lat: Optional[str],
    lon: Optional[str],
    city: Optional[str]
) -> CurrentWeatherResponse:
    if not (lat and lon) and not city:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Either 'city' or ('lat', 'lon') must be provided."
        )

    q_param = city if city else f"{lat},{lon}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{WEATHER_API_BASE_URL}/current.json",
                params={"key": WEATHER_API_KEY, "q": q_param},
                timeout=10.0
            )
            response.raise_for_status()
            return CurrentWeatherResponse(**response.json())

    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        if status_code == HTTPStatus.NOT_FOUND:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="City or coordinates not found.")
        if status_code == HTTPStatus.BAD_REQUEST:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid city or coordinates.")
        raise HTTPException(status_code=e.response.status_code, detail="Weather API error")

    except httpx.RequestError:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail="Service unavailable")

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


async def get_forecast_weather_data(
    lat: Optional[str],
    lon: Optional[str],
    city: Optional[str],
    days: int
) -> ForecastWeatherResponse:
    if not (lat and lon) and not city:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Either 'city' or ('lat', 'lon') must be provided."
        )

    q_param = city if city else f"{lat},{lon}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{WEATHER_API_BASE_URL}/forecast.json",
                params={"key": WEATHER_API_KEY, "q": q_param, "days": days},
                timeout=10.0
            )
            response.raise_for_status()
            return ForecastWeatherResponse(**response.json())

    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        if status_code == HTTPStatus.NOT_FOUND:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="City or coordinates not found.")
        if status_code == HTTPStatus.BAD_REQUEST:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid city or coordinates.")
        raise HTTPException(status_code=e.response.status_code, detail="Weather API error")

    except httpx.RequestError:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail="Service unavailable")

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
