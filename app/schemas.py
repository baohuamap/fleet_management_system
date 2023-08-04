import datetime as dt
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BaseFleet(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    fleet_name: str = Field(alias="name")
    fleet_info: str = Field(alias="info")
    phone_number: str = Field(alias="phone")


class Fleet(BaseFleet):
    id: UUID = Field(alias="uuid")
    date_created: dt.datetime = Field(alias="date")

    class Config:
        from_attributes = True


class CreateFleet(BaseFleet):
    pass


class BaseVehicle(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    vehicle_brand: str = Field(alias="brand")
    vehicle_plate_number: str = Field(alias="plate")


class Vehicle(BaseVehicle):
    id: UUID = Field(alias="uuid")
    date_created: dt.datetime
    owner_id: UUID = Field(alias="owner_uuid")

    class Config:
        from_attributes = True


class CreateVehicle(BaseVehicle):
    pass


class BaseDriver(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    driver_name: str = Field(alias="name")
    phone_number: str = Field(alias="phone")


class Driver(BaseDriver):
    id: UUID = Field(alias="uuid")
    date_created: dt.datetime = Field(alias="date")

    class Config:
        from_attributes = True


class CreateDriver(BaseDriver):
    pass


class BaseRoute(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    route_name: str = Field(alias="name")
    route_info: str = Field(alias="info")


class Route(BaseRoute):
    id: UUID = Field(alias="uuid")
    date_created: dt.datetime = Field(alias="date")
    driver_id: UUID = Field(alias="driver_uuid")
    vehicle_id: UUID = Field(alias="vehicle_uuid")

    class Config:
        from_attributes = True


class CreateRoute(BaseRoute):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
