from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from what_to_wear.api.services.weather_service import get_current_weather_data, get_forecast_weather_data
from what_to_wear.api.models.schemas.weather_request_params import WeatherRequestParams, ForecastWeatherRequestParams

router = APIRouter()


@router.get("/current")
async def get_current_weather(params: WeatherRequestParams = Depends()) -> JSONResponse:
    """ Fetches weather data for current conditions. """
    try:
        weather_data = await get_current_weather_data(params.lat, params.lon)
        return JSONResponse(status_code=HTTPStatus.OK, content=weather_data)

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Error fetching weather data: {e}")


@router.get("/forecast")
async def get_forecast_weather(params: ForecastWeatherRequestParams = Depends()) -> JSONResponse:
    """ Fetches weather forecast data. """
    try:
        weather_data = await get_forecast_weather_data(params.lat, params.lon, params.days)
        return JSONResponse(status_code=HTTPStatus.OK, content=weather_data)

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Error fetching forecast weather data: {e}")
