from typing import Any
from fastapi import FastAPI, HTTPException,status
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


shipments = {
    12701: {
        "weight": 0.6,
        "content": "glassware",
        "status": "placed"
    },
    12702: {
        "weight": 12.5,
        "content": "monitor",
        "status": "shipped"
    },
    12703: {
        "weight": 1.2,
        "content": "keyboard",
        "status": "pending"
    },
    12704: {
        "weight": 0.3,
        "content": "cables",
        "status": "delivered"
    },
    12705: {
        "weight": 4.8,
        "content": "printer",
        "status": "processing"
    },
    12706: {
        "weight": 0.1,
        "content": "stickers",
        "status": "placed"
    },
    12707: {
        "weight": 15.0,
        "content": "desk_lamp",
        "status": "cancelled"
    }
}

@app.get("/shipments",status_code=status.HTTP_200_OK)
def get_latest_shipment(id: int | None = None)-> dict[str,Any]:
    if not id:
        id = max(shipments.keys)
        return shipments[id]
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Given ID doesn't exist")
    return shipments[id]

@app.post("/shipments")
def submit_shipment(data: dict[str ,Any]) -> dict[str,int]:
    new_id = max(shipments.keys()) + 1

    content : str = data["content"]
    weight : float = data["weight"]

    shipments[new_id] = {
        "content" : content,
        "weight" : weight,
        "status" : "placed"
    }

    return {
        "id" : new_id
    }


@app.get("/shipments/{id}")
def get_shipments(id:int | None = None) -> dict[str,Any]:
    return shipments[id]

@app.get("/shipment/{field}")
def get_shipment_field(field:str,id: int) -> dict[str,Any]:
    return {
        field: shipments[id][field]
    }


@app.get("/documents",include_in_schema=False)
def get_docs():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title="Scalar API"
    )