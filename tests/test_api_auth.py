import httpx
import pytest

from bit.database import connect
from bit.endpoints.api import auth_app
from tests.conftest import Fuzzy


@pytest.fixture()
async def client(database):
    auth_app.dependency_overrides[connect] = lambda: database
    async with httpx.AsyncClient(app=auth_app, base_url="http://localhost") as client:
        yield client


@pytest.mark.asyncio
async def test_user_authentication(client):
    response = await client.post("/login", json={"username": "Bob"})
    assert response.status_code == 200
    assert response.json() == {"access_token": Fuzzy(str)}
