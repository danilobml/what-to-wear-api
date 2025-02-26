from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel import Session, select

from what_to_wear.api.database.db import get_session
from what_to_wear.api.models.db_models.user import User
from what_to_wear.api.models.schemas.jwt import TokenData
from what_to_wear.api.utils.constants import ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def create_user(username: str, password: str, session: Session):
    """Creates a new user with a hashed password."""
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    """Verifies a password against its hashed version."""
    return pwd_context.verify(raw_password, hashed_password)


def get_password_hash(raw_password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(raw_password)


def get_user_by_username(username: str, session: Session) -> User:
    """Retrieves a user by their username from the database."""
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user


def authenticate_user(username: str, password: str, session: Session) -> Union[User, bool]:
    """Authenticates a user by verifying their credentials."""
    user = get_user_by_username(username, session)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Creates a JWT access token with an optional expiration time."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session)
) -> User:
    """Retrieves the current authenticated user from the JWT token."""
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
    user: User = get_user_by_username(token_data.username, session)
    if user is None:
        raise credentials_exception
    return user
