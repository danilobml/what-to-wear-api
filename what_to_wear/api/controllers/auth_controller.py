from datetime import timedelta
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from what_to_wear.api.utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES, UsernameAlreadyExistsException
from what_to_wear.api.models.schemas.jwt import Token
from what_to_wear.api.models.schemas.user_auth import UserAuth
from what_to_wear.api.database.db import get_session
from what_to_wear.api.services.auth_service import (
    authenticate_user,
    create_access_token,
    get_user_by_username,
    create_user
)


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserAuth, session=Depends(get_session)):
    try:
        existing_user = get_user_by_username(user_data.username, session)
        if existing_user:
            raise UsernameAlreadyExistsException()

        await create_user(user_data.username, user_data.password, session)
        return JSONResponse(status_code=HTTPStatus.CREATED, content="User created successfully.")

    except UsernameAlreadyExistsException:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Error creating user: {e}")


@router.post("/login")
async def login_for_access_token(user_data: UserAuth, session=Depends(get_session)) -> Token:
    """ Logs in and returns JWT, if username and password match a DB User """
    user = authenticate_user(user_data.username, user_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
