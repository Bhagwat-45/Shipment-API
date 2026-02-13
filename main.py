from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from routers.shipment_router import router

app = FastAPI()
app.include_router(router)

@app.get("/documents",include_in_schema=False)
def get_docs():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title="Scalar API"
    )
