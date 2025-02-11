from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.requests import Request

router = APIRouter()


@router.get('/')
async def get_test(request: Request) -> JSONResponse:
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={'message': 'Test!'}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed: {e}',
        )
