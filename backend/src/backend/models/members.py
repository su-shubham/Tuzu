from dataclasses import dataclass
from datetime import datetime

from quart_db import Connection


@dataclass
class Members:
    id: int
    email: str
    password_hash: str
    created_at: datetime
    email_verified: datetime | None


async def select_member_by_email(email: str, db: Connection) -> Members | None:
    result = await db.fetch_one(
        """
            SELECT id,email,password_hash,created_at,email_verified
            FROM members
            WHERE LOWER(email) = LOWER(:email)""",
        {"email": email},
    )
    return None if result is None else Members(**result)


async def select_member_by_id(id: int, db: Connection) -> Members | None:
    result = await db.fetch_one(
        """
        SELECT id,email,password_hash,created_at,email_verified
        FROM members
        WHERE id=:id""",
        {"id": id},
    )
    return None if result is None else Members(**result)


async def insert_members(
    email: str, password_hash: str, db: Connection
) -> Members:  # noqa: E501
    result = await db.fetch_one(
        """
        INSERT INTO members(email,password_hash)
            VALUES(:email,:password_hash)
        RETURNING id,email,password_hash,created_at,email_verified""",
        {"email": email, "password_hash": password_hash},
    )
    return Members(**result)


async def update_member_password(
    id: int, password_hash: str, db: Connection
) -> None:  # noqa: E501
    await db.execute(
        """
        UPDATE members
            SET password_hash = :password_hash
            WHERE id = :id""",
        {"id": id, "password_hash": password_hash},
    )


async def update_member_email(id: int, db: Connection) -> None:
    await db.execute(
        """
        UPDATE members
            SET email_verified = now() WHERE id = :id """,
        {"id": id},
    )
