from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from what_to_wear.api.models.schemas.weather_request_params import (
    ForecastWeatherRequestParams,
    WeatherRequestParams,
)
from what_to_wear.api.services.auth_service import get_current_user
from what_to_wear.api.services.recommendation_service import get_llm_recommendation
from what_to_wear.api.services.weather_service import (
    get_current_weather_data,
    get_forecast_weather_data,
)
from what_to_wear.api.utils.constants import RequestTypeEnum

router = APIRouter()


@router.get("/current", response_model=str)
async def get_current_recommendation(
    params: WeatherRequestParams = Depends(),
    current_user: dict = Depends(get_current_user)
) -> JSONResponse:
    try:
        weather_data = await get_current_weather_data(params.lat, params.lon, params.city)
        recommendation = await get_llm_recommendation(weather_data, RequestTypeEnum.CURRENT)
        return JSONResponse(status_code=HTTPStatus.OK, content=recommendation)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/forecast", response_model=str)
async def get_forecast_recommendation(
    params: ForecastWeatherRequestParams = Depends(),
    current_user: dict = Depends(get_current_user)
) -> JSONResponse:
    try:
        weather_data = await get_forecast_weather_data(params.lat, params.lon, params.city, params.days)
        recommendation = await get_llm_recommendation(weather_data, RequestTypeEnum.FORECAST)
        return JSONResponse(status_code=HTTPStatus.OK, content=recommendation)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
