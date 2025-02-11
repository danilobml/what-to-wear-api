from fastapi import APIRouter

from ..api.controllers import test

router = APIRouter()

router.include_router(test.router, prefix='/test', tags=['test'])
