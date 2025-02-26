from fastapi import APIRouter

from .controllers import auth_controller, recommendation_controller, weather_controller

router = APIRouter()

router.include_router(weather_controller.router, prefix='/weather', tags=['weather'])
router.include_router(recommendation_controller.router, prefix='/recommendation', tags=['recommendation'])
router.include_router(auth_controller.router, prefix='/auth', tags=['auth'])
