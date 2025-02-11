from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from what_to_wear.api.services.weather_service import get_current_weather_data
from what_to_wear.api.services.recommendation_service import get_llm_recommendation


router = APIRouter()


@router.get("/latlon/{lat}/{lon}")
async def get_recommendations(lat: str, lon: str) -> JSONResponse:
    try:
        weather_data = await get_current_weather_data(lat, lon)
        print(weather_data)
        response = await get_llm_recommendation(weather_data)
        return JSONResponse(status_code=HTTPStatus.OK, content=response)

    except Exception as e:
        return HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Error fetching current weather data: {e}")
