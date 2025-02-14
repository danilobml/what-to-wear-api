from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError

from what_to_wear.api.utils.constants import SECRET_KEY, ALGORITHM
from what_to_wear.api.models.db_models.user import User
from what_to_wear.api.models.schemas.jwt import TokenData
from what_to_wear.api.database.db import get_session


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def create_user(username: str, password: str, session: Session):
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


def get_password_hash(raw_password: str) -> str:
    return pwd_context.hash(raw_password)


def get_user_by_username(username: str, session: Session) -> User:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user


def authenticate_user(username: str, password: str, session: Session) -> Union[User, bool]:
    user = get_user_by_username(username, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
            token: Annotated[str, Depends(oauth2_scheme)],
            session: Session = Depends(get_session)
        ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(token_data.username, session)
    if user is None:
        raise credentials_exception
    return user
