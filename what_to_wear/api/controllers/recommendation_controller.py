from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from what_to_wear.api.services.weather_service import get_current_weather_data, get_forecast_weather_data
from what_to_wear.api.services.recommendation_service import get_llm_recommendation
from what_to_wear.api.utils.constants import RequestTypeEnum
from what_to_wear.api.models.schemas.weather_request_params import WeatherRequestParams, ForecastWeatherRequestParams

router = APIRouter()


@router.get("/current")
async def get_current_recommendation(params: WeatherRequestParams = Depends()) -> JSONResponse:
    """ Fetches LLM-based clothing recommendations based on current weather. """
    try:
        weather_data = await get_current_weather_data(params.lat, params.lon)
        recommendation = await get_llm_recommendation(weather_data, RequestTypeEnum.CURRENT)
        return JSONResponse(status_code=HTTPStatus.OK, content=recommendation)

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Error generating recommendation: {e}")


@router.get("/forecast")
async def get_forecast_recommendation(params: ForecastWeatherRequestParams = Depends()) -> JSONResponse:
    """ Fetches LLM-based clothing recommendations based on forecast weather. """
    try:
        weather_data = await get_forecast_weather_data(params.lat, params.lon, params.days)
        recommendation = await get_llm_recommendation(weather_data, RequestTypeEnum.FORECAST)
        return JSONResponse(status_code=HTTPStatus.OK, content=recommendation)

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Error generating recommendation: {e}")
