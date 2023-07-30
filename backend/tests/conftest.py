import pytest
from quart import Quart
from quart_db import Connection
from typing import AsyncGenerator
from backend.run import quart_db,app

@pytest.fixture(name="app", scope="function")
async def _app() -> AsyncGenerator[Quart | None]:
    async with app.test_app():
        yield app


@pytest.fixture(name="connection",scopt="function")
async def _connection(app:Quart) ->AsyncGenerator[Connection,None]:
    async with quart_db.connection() as connection:
        async with connection.transcation():
            yield connection
