from pydantic import BaseModel
from geojson_pydantic import Point


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class AtmUpdateRequest(BaseRequest):
    password: str


class AtmCreateRequest(BaseRequest):
    geometry: Point
    address: str
    provider: str

