"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""
import uuid

from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from geoalchemy2 import Geometry

class Base(DeclarativeBase):
    pass


class Atm(Base):
    __tablename__ = "atm"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    geom: Mapped[str] = mapped_column(
        Geometry(geometry_type='POINT', srid=4326), nullable=True
    )
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self):
        return "id:% s geom:% s address:% s provider:% s" % (self.id, self.geom, self.address, self.provider)

