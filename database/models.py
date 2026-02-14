from datetime import datetime
from sqlmodel import SQLModel,Field
from enum import Enum

class ShipmentStatus(str,Enum):
    place = "placed"
    in_transit ="in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class Shipment(SQLModel,table=True):
    __tablename__ = "shipment"

    id : int = Field(default=None,primary_key=True)
    content : str
    weight : float = Field(le=25)
    destination : int
    status : ShipmentStatus
    esitmated_delivery : datetime