import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, status
from uuid import uuid4
from datetime import datetime, timezone

from app.auth.dependencies import get_current_user, get_current_active_user
from app.schemas.user import UserResponse
from app.models.user import User


def make_user(is_active=True):
    """Build a real (unpersisted) User ORM instance for mocking db.query(...).first()."""
    return User(
        id=uuid4(),
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="hashed",
        is_active=is_active,
        is_verified=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_verify_token():
    with patch.object(User, "verify_token") as mock:
        yield mock


def test_get_current_user_valid_token_existing_user(mock_verify_token, mock_db):
    user = make_user()
    mock_verify_token.return_value = user.id
    mock_db.query.return_value.filter.return_value.first.return_value = user

    result = get_current_user(token="validtoken", db=mock_db)

    assert isinstance(result, UserResponse)
    assert result.id == user.id
    assert result.username == user.username
    assert result.email == user.email
    assert result.first_name == user.first_name
    assert result.last_name == user.last_name
    assert result.is_active == user.is_active
    assert result.is_verified == user.is_verified

    mock_verify_token.assert_called_once_with("validtoken")


def test_get_current_user_invalid_token(mock_verify_token, mock_db):
    mock_verify_token.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token="invalidtoken", db=mock_db)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"
    mock_verify_token.assert_called_once_with("invalidtoken")


def test_get_current_user_valid_token_user_not_found_in_db(mock_verify_token, mock_db):
    """Token decodes fine, but the user no longer exists in the DB (e.g. deleted after issuance)."""
    mock_verify_token.return_value = uuid4()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token="validtoken", db=mock_db)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"


def test_get_current_active_user_active(mock_verify_token, mock_db):
    user = make_user(is_active=True)
    mock_verify_token.return_value = user.id
    mock_db.query.return_value.filter.return_value.first.return_value = user

    current_user = get_current_user(token="validtoken", db=mock_db)
    active_user = get_current_active_user(current_user=current_user)

    assert isinstance(active_user, UserResponse)
    assert active_user.is_active is True


def test_get_current_active_user_inactive(mock_verify_token, mock_db):
    user = make_user(is_active=False)
    mock_verify_token.return_value = user.id
    mock_db.query.return_value.filter.return_value.first.return_value = user

    current_user = get_current_user(token="validtoken", db=mock_db)

    with pytest.raises(HTTPException) as exc_info:
        get_current_active_user(current_user=current_user)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Inactive user"
