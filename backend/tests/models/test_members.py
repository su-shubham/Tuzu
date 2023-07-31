import pytest
from asyncpg.exceptions import UniqueViolationError
from quart_db import Connection
from backend.models.members import insert_members,select_member_by_email

async def test_insert_members(connection:Connection) ->None:
    await insert_members(connection,"shubham@tozo.co","")
    with pytest.raises(UniqueViolationError):
        await insert_members(connection,"Shubham@toooz.co","")

async def test_select_member_by_email(connection:Connection) ->None:
    await insert_members(connection,"shubham@tozo.co","")
    members = await select_member_by_email(
        connection,"Shubham@tozo.co",
    )
    assert members is not None
