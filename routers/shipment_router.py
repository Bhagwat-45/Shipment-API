from fastapi import APIRouter,HTTPException,status
from typing import Optional,Any
from data import shipments
from schema.shipment_schema import ShipmentCreate, ShipmentRead, ShipmentStatus, ShipmentUpdate
from database.database import Database

router = APIRouter(
    tags=["Shipments"],
    prefix="/api"
)

db = Database()

@router.get("/shipments",status_code=status.HTTP_200_OK,response_model=ShipmentRead)
def get_shipment(id: int):
    shipment = db.get_shipment(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Given Id doesn't exist!"
        )
    
    return shipment


@router.post("/shipments",status_code=status.HTTP_201_CREATED,response_model=None)
def new_shipment(shipment: ShipmentCreate):
    new_id = db.create_shipment(shipment)

    return {"id" : new_id}


@router.patch("/shipments",response_model=ShipmentRead)
def update_shipments(
    id: int,shipment: ShipmentUpdate
):
    shipment = db.update_shipment(id,shipment)

    return shipment


@router.delete("/shipments",status_code=status.HTTP_200_OK,response_model=None)
def delete_shipment(id: int):
    db.delete(id)
    return {
        "detail" : f"The shipment with id {id} was deleted"
    }