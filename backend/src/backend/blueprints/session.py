from dataclasses import dataclass
from datetime import timedelta

import bcrypt
from pydantic import EmailStr
from quart import ResponseReturnValue, g
from quart.blueprints import Blueprint
from quart_auth import (  # noqa: E501
    AuthUser,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from quart_rate_limiter import rate_exempt, rate_limit
from quart_schema import validate_request, validate_response

from backend.lib.api_error import APIError
from backend.models.members import select_member_by_email

blueprint = Blueprint("session", __name__)


@dataclass
class LoginData:
    email: EmailStr
    password: str
    remember: bool = False


@dataclass
class Status:
    member_id: int


@blueprint.post("/session/")
@rate_limit(5, timedelta(minutes=1))
@validate_request(LoginData)
async def login_users(data: LoginData) -> ResponseReturnValue:
    result = await select_member_by_email(data.email, g.connection)
    if result is None:
        raise APIError(401, "INVALID CREDENTIALS")
    password_matched = bcrypt.checkpw(
        data.password.encode("utf-8"), result.password_hash.encode("utf-8")
    )
    if password_matched:
        login_user(AuthUser(str(result.id)), data.remember)
        return {}, 200
    else:
        raise APIError(401, "INVALID PASSWORD")


@blueprint.delete("/session/")
@rate_exempt
async def logout() -> ResponseReturnValue:
    logout_user()
    return {}


@blueprint.get("/session/")
@rate_limit(10, timedelta(minutes=1))
@login_required
@validate_response(Status)
async def status() -> ResponseReturnValue:
    assert current_user.auth_id is not None  # nosec
    return Status(member_id=int(current_user.auth_id))
