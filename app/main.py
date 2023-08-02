from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from app import database
from app.routers import drivers, fleets, routes, vehicles

database.add_tables()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fleets.router)
app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(routes.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# test route
@app.get("/", tags=["TEST"])
async def root():
    return {"message": "Hello World! a"}


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
