from fastapi import FastAPI
from sqlalchemy.orm import Session

# from app import database, schemas, services
from app.routers import drivers, fleets, routes, vehicles

app = FastAPI()

app.include_router(fleets.router)
app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(routes.router)


# test route
@app.get("/", tags=["TEST"])
async def root():
    return {"message": "Hello World!"}
