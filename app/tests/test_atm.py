from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import Atm


async def test_create_new_atm(
    client: AsyncClient, default_atm: Atm
):
    response = await client.post(
        app.url_path_for("create_new_atm"),
        json={"id": 21634,
              "geometry": {
                  "type": "Point",
                  "coordinates": [49.2849777, -123.1189405]
              },
              "address": "Han1",
              "provider": "ab"
              },
    )
    assert response.status_code == 201
    result = response.json()
    assert result["id"] == result["id"]
    assert result["address"] == "Han1"

'''
WIP

async def test_get_all_atm(
    client: AsyncClient, default_atm: Atm, session: AsyncSession
):
    atm1 = Atm(id=default_atm.id, address="Han1")
    atm2 = Atm(id=default_atm.id, address="Han2")
    session.add(atm1)
    session.add(atm2)
    await session.commit()

    response = await client.get(
        app.url_path_for("get_all_atm"),

    )
    assert response.status_code == 200

    assert response.json() == [
        {
            "id": default_atm.id,
            "address": "Han1",
        },
        {
            "id": default_atm.id,
            "address": "Han2",
        },
    ]
'''