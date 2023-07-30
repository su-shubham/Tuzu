import pytest
from asyncpg.exceptions import UniqueViolationError
from quart_db import Connection
from backend.models.members import insert_members,select_member_by_email

async def test_insert_members(connection:Connection) ->None:
    await insert_members(connection,"shubham@toooz.co","")
    with pytest.raises(UniqueViolationError):
        await insert_members(connection,"Shubham@toooz.co","")

async def test_select_member_by_email(connection:Connection) ->None:
    await insert_members(connection,"shubham@toooz.co","")
    members = await select_member_by_email(
        connection,"Shubham@toooz.co",
    )
    assert members is not None
