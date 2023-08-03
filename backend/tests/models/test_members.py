import pytest
from asyncpg.exceptions import UniqueViolationError
from quart_db import Connection

from backend.models.members import insert_members, select_member_by_email


async def test_insert_members(connection: Connection) -> None:
    await insert_members("shubham@tozo.co", "", connection)
    with pytest.raises(UniqueViolationError):
        await insert_members("Shubham@tozo.co", "", connection)


async def test_select_member_by_email(connection: Connection) -> None:
    await insert_members("shubham@tozo.co", "", connection)
    members = await select_member_by_email(
        "Shubham@tozo.co",
        connection,
    )
    assert members is not None
