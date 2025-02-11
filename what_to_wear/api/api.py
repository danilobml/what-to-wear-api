from fastapi import APIRouter

from ..api.controllers import weather_controller, recommendation_controller

router = APIRouter()

router.include_router(weather_controller.router, prefix='/weather', tags=['test'])
router.include_router(recommendation_controller.router, prefix='/recommendation', tags=['test'])
