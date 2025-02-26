from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from unittest.mock import MagicMock

import jwt
import pytest
from fastapi import HTTPException
from sqlmodel import Session

from what_to_wear.api.models.db_models.user import User
from what_to_wear.api.services.auth_service import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    get_user_by_username,
    verify_password,
)
from what_to_wear.api.utils.constants import ALGORITHM, SECRET_KEY


@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)


@pytest.fixture
def test_user():
    return User(username="testuser", hashed_password=get_password_hash("testpassword"))


def test_verify_password():
    raw_password = "testpassword"
    hashed_password = get_password_hash(raw_password)
    assert verify_password(raw_password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False


def test_get_password_hash():
    raw_password = "securepassword"
    hashed_password = get_password_hash(raw_password)
    assert isinstance(hashed_password, str)
    assert hashed_password != raw_password


def test_get_user_by_username(mock_session, test_user):
    mock_session.exec.return_value.first.return_value = test_user
    user = get_user_by_username("testuser", mock_session)
    assert user.username == "testuser"


def test_authenticate_user_success(mock_session, test_user):
    mock_session.exec.return_value.first.return_value = test_user
    user = authenticate_user("testuser", "testpassword", mock_session)
    assert user is not False
    assert user.username == "testuser"


def test_authenticate_user_failure(mock_session):
    mock_session.exec.return_value.first.return_value = None
    user = authenticate_user("invaliduser", "wrongpassword", mock_session)
    assert user is False


def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "testuser"
    assert "exp" in decoded


def test_create_access_token_expiry():
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=1)
    token = create_access_token(data, expires_delta)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    expiration = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    assert expiration > datetime.now(timezone.utc)


@pytest.mark.asyncio
async def test_get_current_user_success(mock_session, test_user):
    token = create_access_token({"sub": "testuser"})
    mock_session.exec.return_value.first.return_value = test_user
    user = await get_current_user(token, mock_session)
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(mock_session):
    invalid_token = "invalid.jwt.token"
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(invalid_token, mock_session)
    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert "Could not validate credentials" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_expired_token(mock_session):
    expired_token = create_access_token({"sub": "testuser"}, expires_delta=timedelta(seconds=-1))
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(expired_token, mock_session)
    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert "Could not validate credentials" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_nonexistent_user(mock_session):
    token = create_access_token({"sub": "nonexistentuser"})
    mock_session.exec.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token, mock_session)
    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert "Could not validate credentials" in exc_info.value.detail
