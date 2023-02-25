import time
from collections.abc import AsyncGenerator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core import config
from app.core.session import async_session
from app.models import Atm

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/access-token")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_atm(
    session: AsyncSession = Depends(get_session), token: str = Depends(reusable_oauth2)
) -> List[Atm]:

    result = await session.query(Atm).all()


    if not result:
        raise HTTPException(status_code=404, detail="Empty")
    return result
