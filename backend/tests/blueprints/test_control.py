from quart import Quart


async def test_control(app: Quart) -> str:
    test_client = app.test_client()
    response = await test_client.get("/control")
    assert (await response.get_json())["ping"] == "control"
