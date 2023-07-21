from typing import List

import sqlalchemy.orm as orm
from fastapi import APIRouter, Depends, FastAPI, HTTPException

import schemas
import services

app = FastAPI()
fleets_router = APIRouter()
vehicles_router = APIRouter()
drivers_router = APIRouter()
routes_router = APIRouter()


# add tables
services.add_tables()

# fleets methods
@fleets_router.post(
    "/", tags=["Fleets"], response_model=schemas.Fleet
)
async def create_fleet(
    fleet: schemas.CreateFleet, db: orm.Session = Depends(services.get_db)
):
    return await services.create_fleet(fleet=fleet, db=db)


@fleets_router.get(
    "/", tags=["Fleets"],  response_model=List[schemas.Fleet]
)
async def get_fleets(
    db: orm.Session = Depends(services.get_db)
):
    return await services.get_all_fleets(db=db)


@fleets_router.get(
    "/{fleet_id}", tags=["Fleets"], response_model=schemas.Fleet
)
async def get_fleet(
    fleet_id, db: orm.Session = Depends(services.get_db)
):
    fleet = await services.get_fleet(fleet_id=fleet_id, db=db)
    if fleet is None:
        raise HTTPException(
            status_code=404, detail="Fleet does not exist"
        )
    return fleet


@fleets_router.delete(
    "/{fleet_id}", tags=["Fleets"]
)
async def delete_fleet(
    fleet_id, db: orm.Session = Depends(services.get_db)
):
    fleet = await services.get_fleet(fleet_id=fleet_id, db=db)
    if fleet is None:
        raise HTTPException(
            status_code=404, detail="Fleet does not exist"
        )
    await services.delete_fleet(fleet=fleet, db=db)
    return f"Successfully delete the Fleet with id {fleet_id}"


@fleets_router.put(
    "/{fleet_id}", tags=["Fleets"], response_model=schemas.Fleet
)
async def update_fleet(
    fleet_id: int, fleet_data: schemas.CreateFleet, db: orm.Session = Depends(services.get_db)
):
    fleet = await services.get_fleet(fleet_id=fleet_id, db=db)
    if fleet is None:
        raise HTTPException(
            status_code=404, detail="Fleet does not exist"
        )
    return await services.update_fleet(
        fleet_data=fleet_data, fleet=fleet, db=db
    )


app.include_router(fleets_router, prefix="/api/fleets")


# vehicles methods
@vehicles_router.post(
    "/", tags=["Vehicles"], response_model=schemas.Vehicle
)
async def create_vehicle(
    vehicle: schemas.CreateVehicle,
    fleet_id: int,
    db: orm.Session = Depends(services.get_db)
):
    fleet = await services.get_fleet(fleet_id=fleet_id, db=db)
    if fleet is None:
        raise HTTPException(
            status_code=404, detail="Fleet does not exist"
        )
    return await services.create_vehicle(
        vehicle=vehicle, owner_id=fleet_id, db=db
    )


@vehicles_router.get(
    "/", tags=["Vehicles"], response_model=List[schemas.Vehicle]
)
async def get_vehicles(
    db: orm.Session = Depends(services.get_db)
):
    return await services.get_all_vehicles(db=db)


@vehicles_router.get(
    "/fleet/{fleet_id}", tags=["Vehicles"], response_model=List[schemas.Vehicle]
)
async def get_vehicles_in_fleet(
    fleet_id, db: orm.Session = Depends(services.get_db)
):
    return await services.get_all_vehicles_in_fleet(
        fleet_id=fleet_id, db=db
    )


@vehicles_router.get(
    "/{vehicle_id}", tags=["Vehicles"], response_model=schemas.Vehicle
)
async def get_vehicle(
    vehicle_id, db: orm.Session = Depends(services.get_db)
):
    vehicle = await services.get_vehicle(vehicle_id=vehicle_id, db=db)
    if vehicle is None:
        raise HTTPException(
            status_code=404, detail="Vehicle does not exist"
        )
    return vehicle


@vehicles_router.delete(
    "/{vehicle_id}", tags=["Vehicles"]
)
async def delete_vehicle(
    vehicle_id, db: orm.Session = Depends(services.get_db)
):
    vehicle = await services.get_vehicle(vehicle_id=vehicle_id, db=db)
    if vehicle is None:
        raise HTTPException(
            status_code=404, detail=f"Vehicle {vehicle_id} does not exist"
        )
    await services.delete_vehicle(vehicle=vehicle, db=db)
    return f"Successfully delete the Vehicle with id {vehicle_id}"


@vehicles_router.put(
    "/{vehicle_id}", tags=["Vehicles"], response_model=schemas.Vehicle
)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: schemas.CreateVehicle,
    db: orm.Session = Depends(services.get_db)
):
    vehicle = await services.get_vehicle(vehicle_id=vehicle_id, db=db)
    if vehicle is None:
        raise HTTPException(
            status_code=404, detail="Vehicle does not exist"
        )
    return await services.update_vehicle(
        vehicle_data=vehicle_data, vehicle=vehicle, db=db
    )


app.include_router(vehicles_router, prefix="/api/vehicles")


# drivers methods
@drivers_router.post(
    "/", tags=["Drivers"], response_model=schemas.Driver
)
async def create_driver(
    driver: schemas.CreateDriver, db: orm.Session = Depends(services.get_db)
):
    return await services.create_driver(driver=driver, db=db)


@drivers_router.get(
    "/", tags=["Drivers"], response_model=List[schemas.Driver]
    )
async def get_drivers(
    db: orm.Session = Depends(services.get_db)
):
    return await services.get_all_drivers(db=db)


@drivers_router.get(
    "/{driver_id}", tags=["Drivers"], response_model=schemas.Driver
)
async def get_driver(
    driver_id, db: orm.Session = Depends(services.get_db)
):
    driver = await services.get_driver(driver_id=driver_id, db=db)
    if driver is None:
        raise HTTPException(
            status_code=404, detail="Driver does not exist"
        )
    return driver


@drivers_router.delete(
    "/{driver_id}", tags=["Drivers"]
)
async def delete_driver(
    driver_id, db: orm.Session = Depends(services.get_db)
):
    driver = await services.get_driver(driver_id=driver_id, db=db)
    if driver is None:
        raise HTTPException(
            status_code=404, detail=f"Driver {driver_id} does not exist"
        )
    await services.delete_driver(driver=driver, db=db)
    return f"Successfully delete the Driver with id {driver_id}"


@drivers_router.put(
    "/{driver_id}", tags=["Drivers"], response_model=schemas.Driver
)
async def update_driver(
    driver_id: int,
    driver_data: schemas.CreateDriver,
    db: orm.Session = Depends(services.get_db)
):
    driver = await services.get_driver(driver_id=driver_id, db=db)
    if driver is None:
        raise HTTPException(
            status_code=404, detail="Driver does not exist"
        )
    return await services.update_driver(
        driver_data=driver_data, driver=driver, db=db
    )


app.include_router(drivers_router, prefix="/api/drivers")


# routes methods
@routes_router.post(
    "/", tags=["Routes"], response_model=schemas.Route
)
async def create_route(
    route: schemas.CreateRoute,
    driver_id: int,
    vehicle_id: int,
    db: orm.Session = Depends(services.get_db)
):
    driver = await services.get_driver(driver_id=driver_id, db=db)
    if driver is None:
        raise HTTPException(
            status_code=404, detail=f"Driver {driver_id} does not exist"
        )
    vehicle = await services.get_vehicle(vehicle_id=vehicle_id, db=db)
    if vehicle is None:
        raise HTTPException(
            status_code=404, detail=f"Vehicle {vehicle_id} does not exist"
        )
    return await services.create_route(
        route=route, db=db, driver_id=driver.id, vehicle_id=vehicle.id
    )


@routes_router.get(
    "/", tags=["Routes"], response_model=List[schemas.Route]
)
async def get_routes(
    db: orm.Session = Depends(services.get_db)
):
    return await services.get_all_routes(db=db)


@routes_router.get(
    "/{route_id}", tags=["Routes"], response_model=schemas.Route
)
async def get_route(
    route_id, db: orm.Session = Depends(services.get_db)
):
    route = await services.get_route(route_id=route_id, db=db)
    if route is None:
        raise HTTPException(status_code=404, detail="Route does not exist")
    return route



@routes_router.delete(
    "/{route_id}", tags=["Routes"]
)
async def delete_route(
    route_id, db: orm.Session = Depends(services.get_db)
):
    route = await services.get_route(route_id=route_id, db=db)
    if route is None:
        raise HTTPException(
            status_code=404, detail="Route does not exist"
        )
    await services.delete_route(route=route, db=db)
    return f"Successfully delete the Route with id {route_id}"


@routes_router.put(
    "/{route_id}", tags=["Routes"], response_model=schemas.Route
)
async def update_route(
    route_id: int,
    route_data: schemas.CreateRoute,
    db: orm.Session = Depends(services.get_db)
):
    route = await services.get_route(route_id=route_id, db=db)
    if route is None:
        raise HTTPException(
            status_code=404, detail="Route does not exist"
        )
    return await services.update_route(
        route=route, route_data=route_data, db=db
    )


app.include_router(routes_router, prefix="/api/routes")
