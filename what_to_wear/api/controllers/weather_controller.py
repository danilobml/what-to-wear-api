from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from what_to_wear.api.models.schemas.current_weather import CurrentWeatherResponse
from what_to_wear.api.models.schemas.forecast_weather import ForecastWeatherResponse
from what_to_wear.api.models.schemas.weather_request_params import (
    ForecastWeatherRequestParams,
    WeatherRequestParams,
)
from what_to_wear.api.services.auth_service import get_current_user
from what_to_wear.api.services.weather_service import (
    get_current_weather_data,
    get_forecast_weather_data,
)

router = APIRouter()


@router.get("/current", response_model=CurrentWeatherResponse)
async def get_current_weather(
    params: WeatherRequestParams = Depends(),
    current_user: dict = Depends(get_current_user)
) -> JSONResponse:
    try:
        weather_data = await get_current_weather_data(params.lat, params.lon, params.city)
        return JSONResponse(status_code=HTTPStatus.OK, content=weather_data.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Error fetching weather data: {e}")


@router.get("/forecast", response_model=ForecastWeatherResponse)
async def get_forecast_weather(
    params: ForecastWeatherRequestParams = Depends(),
    current_user: dict = Depends(get_current_user)
) -> JSONResponse:
    try:
        weather_data = await get_forecast_weather_data(params.lat, params.lon, params.city, params.days)
        return JSONResponse(status_code=HTTPStatus.OK, content=weather_data.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=f"Error fetching forecast weather data: {e}")
