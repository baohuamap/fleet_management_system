from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import add_tables
from app.routers import drivers, fleets, routes, user, vehicles
from app.security.oauth2 import verify_access_token

add_tables()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(fleets.router)
app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(routes.router)


# test route
@app.get("/", tags=["TEST"], dependencies=[Depends(verify_access_token)])
async def root():
    return {"message": "Hello World!"}
