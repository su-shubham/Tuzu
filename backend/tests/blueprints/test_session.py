from quart import Quart


async def test_session_flow(app, test_client: Quart) -> None:
    await test_client.post(
        "/session/", json={"email": "shubham@tozo.co", "password": "password"}
    )
    response = await test_client.get("/session/")
    # assert (await response.get_json())["memberId"] == 1
    response = await test_client.delete("/session/")
    assert response.status_code == 200


async def test_check_password(app, test_client: Quart) -> None:
    await test_client.post(
        "/session/", json={"email": "shubham@tozo.co", "password": "error"}
    )
    response = await test_client.get("/session/")
    assert response.status_code == 500
