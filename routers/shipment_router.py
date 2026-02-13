from fastapi import APIRouter,HTTPException,status
from typing import Optional,Any
from data import shipments
from schema.shipment_schema import ShipmentCreate, ShipmentRead, ShipmentStatus, ShipmentUpdate

router = APIRouter(
    tags=["Shipments"],
    prefix="/api"
)

@router.get("/shipments",status_code=status.HTTP_200_OK,response_model=ShipmentRead)
def get_latest_shipment(id: Optional[int]):
    if not id:
        latest = max(shipments.keys())
        return shipments[latest]
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return shipments[id]

@router.get("/shipments/{id}",status_code=status.HTTP_200_OK,response_model=ShipmentRead)
def get_shipment_by_id(id: int):
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return shipments[id]

@router.get("/shipments/{field}",status_code=status.HTTP_200_OK,response_model=ShipmentRead)
def get_shipment_by_field(field:str, id: int):
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {
        "field" : shipments[id][field]
    }


@router.post("/shipments",status_code=status.HTTP_201_CREATED,response_model=ShipmentRead)
def new_shipment(body: ShipmentCreate):
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content" : body.content,
        "weight" : body.weight,
        "status" : "placed"
    }

    return {
        "new_shipment" : shipments[new_id]
    }

@router.put("/shipments",response_model=ShipmentRead)
def update_shipments(
    id: int,body: ShipmentUpdate
):
    if id not in shipments:
        raise HTTPException(status_code=404,detail="ID not found!")
    shipments[id] = {
        "content" : body.content,
        "weight" : body.weight,
        "status" : status
    }

    return shipments[id]

@router.patch("/shipments",response_model=ShipmentRead)
def patch_shipments(id:int, body: dict[str,ShipmentStatus]):
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    shipment = shipments[id]

    shipment.update(body)

    shipments[id] = shipment

    return shipment


@router.delete("/shipments",status_code=status.HTTP_200_OK,response_model=ShipmentRead)
def delete_shipment(id: int):
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The shipment id {id} not found!")   
    shipments.pop(id)
    return {
        "detail" : f"The shipment with id {id} was deleted"
    }