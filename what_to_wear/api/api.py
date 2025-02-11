from fastapi import APIRouter

from ..api.controllers import weather_controller

router = APIRouter()

router.include_router(weather_controller.router, prefix='/weather', tags=['test'])
