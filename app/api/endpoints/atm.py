from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Atm
from app.schemas.requests import AtmCreateRequest, AtmUpdateRequest
from app.schemas.responses import AtmResponse, OkResponse
from uuid import uuid4
from shapely.geometry import shape
from sqlalchemy import text
router = APIRouter()



@router.get("/", response_model=list[AtmResponse], status_code=200)
async def get_all_atm(
    session: AsyncSession = Depends(deps.get_session)
):
    """Get all atm"""
    stmt = select(Atm)
    atms = await session.execute(stmt)
    res = atms.scalars()

    #textual_sql = text("SELECT id, ST_AsGeoJSON(geom) as  geom, address, provider from atm")
    #textual_sql = textual_sql.columns(Atm.id, Atm.address, Atm.provider)
    #orm_sql = select(Atm).from_statement(textual_sql)
    #atms = await session.execute(orm_sql)
    #res = atms.scalars()

    return res.all()

@router.post("/", status_code=201)
async def create_new_atm(
    new_atm: AtmCreateRequest,
    session: AsyncSession = Depends(deps.get_session)
):
    """Creates new atm."""
    atm = Atm(id=int(str(uuid4().int)[:5]),
              geom='SRID=4326;' + shape(new_atm.geometry).wkt,
              address=new_atm.address,
              provider=new_atm.provider
              )

    session.add(atm)
    await session.commit()

    return atm

@router.put("/{item_id}", status_code=204)
async def update_atm(
    item_id: int,
    new_atm: AtmCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    """Update atm"""

    await session.query(Atm).filter(Atm.id == item_id).update(
        {
            Atm.geometry:new_atm.geometry,
            Atm.address: new_atm.address,
            Atm.provider: new_atm.provider,
        }, synchronize_session = False)
    await session.commit()


@router.delete("/{item_id}", status_code=204)
async def delete_atm(
    item_id: int,
    session: AsyncSession = Depends(deps.get_session),
):
    """Delete atm"""
    await session.execute(delete(Atm).where(Atm.id == item_id))
    await session.commit()
