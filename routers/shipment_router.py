from datetime import datetime, timedelta
from fastapi import APIRouter,HTTPException,status
from database.models import Shipment
from database.session import SessionDep
from schema.shipment_schema import ShipmentCreate, ShipmentRead, ShipmentStatus, ShipmentUpdate
from database.database import Database

router = APIRouter(
    tags=["Shipments"],
    prefix="/api"
)

db = Database()

@router.get("/shipments",status_code=status.HTTP_200_OK,response_model=ShipmentRead)
def get_shipment(id: int, session : SessionDep):
    shipment = session.get(Shipment,id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Given Id doesn't exist!"
        )
    
    return shipment


@router.post("/shipments",status_code=status.HTTP_201_CREATED,response_model=None)
def new_shipment(shipment: ShipmentCreate, session : SessionDep):
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.place,
        esitmated_delivery=datetime.now() + timedelta(days=3)
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return {"id" : new_shipment.id}


@router.patch("/shipments",response_model=ShipmentRead)
def update_shipments(
    id: int,shipment_update: ShipmentUpdate, session: SessionDep
):
    update = shipment_update.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update"
        )
    shipment = session.get(Shipment,id)
    shipment.sqlmodel_update(update)
    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


@router.delete("/shipments",status_code=status.HTTP_200_OK,response_model=None)
def delete_shipment(id: int,session: SessionDep):
    session.delete(session.get(Shipment,id))
    return {
        "detail" : f"The shipment with id {id} was deleted"
    }