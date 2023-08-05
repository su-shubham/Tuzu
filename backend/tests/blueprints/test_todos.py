from quart import Quart


async def test_get_todo(app: Quart) -> None:
    test_client = app.test_client()
    async with test_client.authenticated("1"):  # type: ignore
        response = await test_client.get("/todos/1/")
        assert response.status_code == 200
        assert (await response.get_json())["task"] == "Test Task"
