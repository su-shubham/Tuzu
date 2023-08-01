from backend.run import app


async def main() -> str:
    test_client = app.test_client()
    response = await test_client.get("/")
    assert (await response.get_json())["hello"] == "pong"
