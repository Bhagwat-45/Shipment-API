from curses.ascii import HT
from fastapi import APIRouter,HTTPException,status
from typing import Optional,Any
from data import shipments
from schema.shipment_schema import Shipment

router = APIRouter(
    tags=["Shipments"],
    prefix="/api"
)

@router.get("/shipments",status_code=status.HTTP_200_OK)
def get_latest_shipment(id: Optional[int])->dict[str,Any]:
    if not id:
        latest = max(shipments.keys())
        return shipments[latest]
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return shipments[id]

@router.get("/shipments/{id}",status_code=status.HTTP_200_OK)
def get_shipment_by_id(id: int)->dict[str,Any]:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return shipments[id]

@router.get("/shipments/{field}",status_code=status.HTTP_200_OK)
def get_shipment_by_field(field:str, id: int)-> dict[str,Any]:
    if field not in ["content","weight","status"] or id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {
        "field" : shipments[id][field]
    }


@router.post("/shipments",status_code=status.HTTP_201_CREATED)
def new_shipment(body: Shipment) -> dict[str,Any]:
    new_id = max(shipments.keys()) + 1


    if body.weight > 25:
        raise HTTPException(
            status_code= status.HTTP_406_NOT_ACCEPTABLE,
            detail= "Maximum weight is 25 Kgs"
        )

    shipments[new_id] = {
        "content" : body.content,
        "weight" : body.weight,
        "status" : "placed"
    }

    return {
        "new_shipment" : shipments[new_id]
    }

@router.put("/shipments")
def update_shipments(
    id: int,body: Shipment
)->dict[str,Any]:
    if id not in shipments:
        raise HTTPException(status_code=404,detail="ID not found!")
    shipments[id] = {
        "content" : body.content,
        "weight" : body.weight,
        "status" : status
    }

    return shipments[id]

@router.patch("/shipments")
def patch_shipments(id:int, body: dict[str,Any])->dict[str,Any]:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    shipment = shipments[id]

    shipment.update(body)

    shipments[id] = shipment

    return shipment


@router.delete("/shipments",status_code=status.HTTP_200_OK)
def delete_shipment(id: int)->dict[str,Any]:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The shipment id {id} not found!")   
    shipments.pop(id)
    return {
        "detail" : f"The shipment with id {id} was deleted"
    }