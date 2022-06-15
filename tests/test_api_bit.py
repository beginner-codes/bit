from io import BytesIO

import httpx
import pytest

from bit.database import connect
from bit.endpoints.api import bit_app
from tests.conftest import Fuzzy


@pytest.fixture()
async def client(database):
    bit_app.dependency_overrides[connect] = lambda: database
    async with httpx.AsyncClient(app=bit_app, base_url="http://localhost") as client:
        yield client


@pytest.mark.asyncio
async def test_bit_creation(client):
    response = await client.post("/create", json={"name": "Test Bit"})
    assert response.status_code == 200
    assert response.json() == {
        "bit": {
            "id": Fuzzy(int),
            "name": "Test Bit",
            "user_id": Fuzzy(int),
            "archived": False,
        }
    }


@pytest.mark.asyncio
async def test_add_file_to_bit(client):
    response = await client.post("/create", json={"name": "Test Bit"})
    bit = response.json()["bit"]

    response = await client.post(
        f"/{bit['id']}/files/add",
        data={"filename": "testing.py"},
        files={"file": ("test.py", BytesIO(b"print('Hello World')"))},
    )
    assert response.status_code == 200
    assert response.json() == {
        "file": {
            "bit_id": bit["id"],
            "file_id": Fuzzy(int),
            "code_id": Fuzzy(int),
            "name": "testing.py",
            "created": Fuzzy(str),
            "code": "print('Hello World')",
        }
    }


@pytest.mark.asyncio
async def test_add_file_to_non_bit(client):
    response = await client.post(
        "/0/files/add",
        files={"file": BytesIO(b"print('Hello World')")},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Bit not found"}
