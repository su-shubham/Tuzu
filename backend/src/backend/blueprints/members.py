from dataclasses import dataclass
from datetime import timedelta
from typing import cast

import asyncpg
import bcrypt
import zxcvbn
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from pydantic import EmailStr, SecretStr
from quart import Blueprint, ResponseReturnValue, current_app, g
from quart_auth import current_user, login_required
from quart_rate_limiter import rate_limit
from quart_schema import validate_request

from backend.lib.api_error import APIError
from backend.lib.email import send_email
from backend.models.members import (
    insert_members,
    select_member_by_email,
    select_member_by_id,
    update_member_email,
    update_member_password,
)

blueprint = Blueprint("members", __name__)

EMAIL_VERIFICATION_SALT = "email verify"  # nosec
MINIMUM_STRENGTH = 3
FORGOTTEN_PASSWORD = "forgotten password"  # nosec
MAX_TOKEN_PERIOD = int(timedelta(days=30).total_seconds())
MAX_RESET_PERIOD = int(timedelta(hours=24).total_seconds())


@dataclass
class MemberData:
    email: str
    password: SecretStr


@blueprint.post("/members/register/")
# @rate_limit(10, timedelta(seconds=10))
@validate_request(MemberData)
async def register_user(data: MemberData) -> ResponseReturnValue:
    # strength = zxcvbn(data.password.get_secret_value())
    # if strength["score"] < MINIMUM_STRENGTH:
    #     raise APIError(400, "Weak Password")

    hashed_password = bcrypt.hashpw(
        data.password.get_secret_value().encode("utf-8"), bcrypt.gensalt(14)
    )

    try:
        member = await insert_members(
            data.email, hashed_password.decode(), g.connection
        )
    except asyncpg.exceptions.UniqueViolationError:
        pass
    else:
        serializer = URLSafeTimedSerializer(
            current_app.secret_key, EMAIL_VERIFICATION_SALT
        )
        token = serializer.dumps(member.id)
        await send_email(
            member.email,
            "Welcome",
            "welcome.html",
            {"token": token},
        )
        return {}, 201


@dataclass
class TokenData:
    token: str


@blueprint.put("/member/email/")
@rate_limit(5, timedelta(minutes=1))
@validate_request(TokenData)
async def verify_email(data: TokenData) -> ResponseReturnValue:
    serializer = URLSafeTimedSerializer(
        current_app.secret_key, salt=EMAIL_VERIFICATION_SALT
    )
    try:
        member_id = serializer.loads(data.token, max_age=MAX_TOKEN_PERIOD)
    except SignatureExpired:
        raise APIError(403, "TOKEN EXPIRED")
    except BadSignature:
        raise APIError(400, "TOKEN INVALID")
    else:
        await update_member_email(member_id, g.connection)
    return {}


@dataclass
class PasswordData:
    new_password: str
    old_password: str


@blueprint.put("/members/password")
@rate_limit(5, timedelta(minutes=1))
@login_required
@validate_request(PasswordData)
async def update_password(data: PasswordData) -> ResponseReturnValue:
    strength = zxcvbn(data.new_password)
    if strength["score"] < MINIMUM_STRENGTH:
        raise APIError(400, "WEAK PASSWORD")
    member_id = int(cast(str, current_user.auth_id))
    member = await select_member_by_id(member_id, g.connection)
    assert member is not None
    password_match = bcrypt.checkpw(
        data.new_password.encode("utf-8"),
        data.old_password.encode("utf-8"),
    )
    if not password_match:
        raise APIError(401, "PASSWORD NOT MATCHED")

    hashed_password = bcrypt.hashpw(
        data.new_password.encode("utf-8"), bcrypt.gensalt(14)
    )
    await update_member_password(member_id, hashed_password.decode(), g.connection)
    await send_email(member.email, "Password Changed", "password_change.html", {})
    return {}


@dataclass
class ForgotPasswordData:
    email: EmailStr


@blueprint.put("/member/forgot_password/")
@rate_limit(5, timedelta(minutes=1))
@validate_request(ForgotPasswordData)
async def forgot_password(data: ForgotPasswordData) -> ResponseReturnValue:
    member = await select_member_by_email(data.email, g.connection)
    if member is not None:
        serializer = URLSafeTimedSerializer(
            current_app.secret_key, salt=FORGOTTEN_PASSWORD
        )
        token = serializer.dumps(member.id)
        await send_email(
            member.email, "Forgot Password", "forgot_password.html", {"token": token}
        )
    return {}


@dataclass
class ResetPasswordData:
    token: str
    password: str


@blueprint.put("/members/reset_password")
@validate_request(ResetPasswordData)
@rate_limit(5, timedelta(minutes=1))
async def reset_password(data: ResetPasswordData) -> ResponseReturnValue:
    serializer = URLSafeTimedSerializer(current_app.secret_key, salt=FORGOTTEN_PASSWORD)
    try:
        member_id = serializer.loads(data.token, max_age=MAX_RESET_PERIOD)
    except BadSignature:
        raise APIError(400, "TOKEN INVALID")
    else:
        strength = zxcvbn(data.password)
        if strength["score"] < MINIMUM_STRENGTH:
            raise APIError(400, "WEAK PASSWORD")
        hashed_password = bcrypt.hashpw(
            data.password.encode("utf-8"), bcrypt.gensalt(14)
        )
        await update_member_password(member_id, hashed_password.decode(), g.connection)
        member = select_member_by_id(int(cast(str, current_user.auth_id)), g.connection)
        assert member is not None  # nosec
        await send_email(
            member.email,
            "Password Changed",
            "password_change.html",
            {},
        )
    return {}
