from pydantic import BaseModel, Field
from random import randint
from enum import Enum

class ShipmentStatus(str,Enum):
    place = "placed"
    in_transit ="in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class BaseShipment(BaseModel):
    content: str = Field(description="Gives us what it contains",max_length=50)
    weight : float = Field(description="Weight of the package",lt=25,ge=1)


class ShipmentRead(BaseShipment):
    status : ShipmentStatus

class ShipmentCreate(BaseShipment):
    pass
    
class ShipmentUpdate(BaseModel):
    status: ShipmentStatus

