from datetime import datetime
from pydantic import BaseModel, Field
from random import randint
from enum import Enum
from database.models import ShipmentStatus

class BaseShipment(BaseModel):
    content: str = Field(description="Gives us what it contains",max_length=50)
    weight : float = Field(description="Weight of the package",lt=25,ge=1)
    destination : int


class ShipmentRead(BaseShipment):
    status : ShipmentStatus
    estimated_delivery : datetime

class ShipmentCreate(BaseShipment):
    pass
    
class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery : datetime | None = Field(default=None)

