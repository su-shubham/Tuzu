import pytest
from quart import Quart


async def register(app: Quart, caplog: pytest.LogCaptureFixture) -> None:
    test_client = app.test_client()
    data = {"email": "shubham@tozo.co", "password": "test@Password23"}
    await test_client.post("/members/", json=data)
    response = await test_client.post("/session/", json={data})
    assert response.status_code == 200
    assert "Sending welcome.html to shubham@tozo.co" in caplog.text
