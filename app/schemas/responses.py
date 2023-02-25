from pydantic import BaseModel, EmailStr
from geojson_pydantic import Point

class BaseResponse(BaseModel):
    # may define additional fields or config shared across responses
    class Config:
        orm_mode = True


class OkResponse(BaseResponse):
    id: int
    address: str
    provider: str

class AtmResponse(BaseResponse):
    id: int
    address: str
    provider: str
