import datetime as dt

import pydantic


class BaseFleet(pydantic.BaseModel):
    fleet_name: str
    fleet_info: str
    phone_number: str


class Fleet(BaseFleet):
    id: int
    date_created: dt.datetime

    class Config:
        from_attributes = True


class CreateFleet(BaseFleet):
    pass


class BaseVehicle(pydantic.BaseModel):
    vehicle_brand: str
    vehicle_plate_number: str


class Vehicle(BaseVehicle):
    id: int
    date_created: dt.datetime
    owner_id: int

    class Config:
        from_attributes = True


class CreateVehicle(BaseVehicle):
    pass


class BaseDriver(pydantic.BaseModel):
    driver_name: str
    phone_number: str


class Driver(BaseDriver):
    id: int
    date_created: dt.datetime

    class Config:
        from_attributes = True


class CreateDriver(BaseDriver):
    pass


class BaseRoute(pydantic.BaseModel):
    route_name: str
    route_info: str


class Route(BaseRoute):
    id: int
    date_created: dt.datetime
    driver_id: int
    vehicle_id: int

    class Config:
        from_attributes = True


class CreateRoute(BaseRoute):
    pass
