"""
Put here any Python code that must be runned before application startup.
It is included in `init.sh` script.

By defualt `main` create a superuser if not exists
"""

import asyncio

from sqlalchemy import select

from app.core import config
from app.core.session import async_session
from app.models import Atm
from shapely.geometry import shape
from uuid import uuid4

async def main() -> None:
    print("Start initial data")
    async with async_session() as session:
        """Creates new atm."""
        atm = Atm(id=int(str(uuid4().int)[:5]),
                  geom='SRID=4326; POINT(49.2849777,-123.1189405)',
                  address='333 Harrison',
                  provider='ab'
                  )

        session.add(atm)
        await session.commit()
        print("Temporary Atm was created")
        print("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
