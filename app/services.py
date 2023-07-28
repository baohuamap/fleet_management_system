"""
services.py
"""
from typing import TYPE_CHECKING, List

from app import models, schemas
from app.database import Base, SessionLocal, engine

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def add_tables():
    return Base.metadata.create_all(bind=engine)


async def create_fleet(
    fleet: schemas.CreateFleet, db: "Session"
) -> schemas.Fleet:
    fleet = models.Fleet(**fleet.model_dump())
    db.add(fleet)
    db.commit()
    db.refresh(fleet)
    return schemas.Fleet.model_validate(fleet)


async def get_all_fleets(db: "Session") -> List[models.Fleet]:
    fleets = db.query(models.Fleet).all()
    return fleets
    # return list(map(schemas.Fleet.model_validate, fleets))


async def get_fleet(fleet_id: int, db: "Session") -> models.Fleet:
    fleet = db.query(models.Fleet).filter(models.Fleet.id == fleet_id).first()
    return fleet


async def delete_fleet(fleet: models.Fleet, db: "Session"):
    db.delete(fleet)
    db.commit()


async def update_fleet(
    fleet_data, fleet: models.Fleet, db: "Session"
) -> schemas.Fleet:
    fleet.fleet_name = fleet_data.fleet_name
    fleet.fleet_info = fleet_data.fleet_info
    fleet.phone_number = fleet_data.phone_number
    db.commit()
    db.refresh(fleet)
    return schemas.Fleet.model_validate(fleet)


async def create_vehicle(
    vehicle: schemas.CreateVehicle, owner_id, db: "Session"
) -> schemas.Vehicle:
    vehicle = models.Vehicle(**vehicle.model_dump())
    vehicle.owner_id = owner_id
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return schemas.Vehicle.model_validate(vehicle)


async def get_all_vehicles(db: "Session") -> List[schemas.Vehicle]:
    vehicles = db.query(models.Vehicle).all()
    return list(map(schemas.Vehicle.model_validate, vehicles))


async def get_all_vehicles_in_fleet(
    fleet_id: int, db: "Session"
) -> List[schemas.Vehicle]:
    vehicles = (
        db.query(models.Vehicle)
        .filter(models.Vehicle.owner_id == fleet_id)
        .all()
    )
    return list(map(schemas.Vehicle.model_validate, vehicles))


async def get_vehicle(vehicle_id: int, db: "Session") -> models.Vehicle:
    vehicle = (
        db.query(models.Vehicle)
        .filter(models.Vehicle.id == vehicle_id)
        .first()
    )
    return vehicle


async def delete_vehicle(vehicle: models.Vehicle, db: "Session"):
    db.delete(vehicle)
    db.commit()


async def update_vehicle(
    vehicle_data, vehicle: models.Vehicle, db: "Session"
) -> schemas.Vehicle:
    vehicle.vehicle_brand = vehicle_data.vehicle_brand
    vehicle.vehicle_plate_number = vehicle_data.vehicle_plate_number
    db.commit()
    db.refresh(vehicle)
    return schemas.Vehicle.model_validate(vehicle)


async def create_driver(
    driver: schemas.CreateDriver, db: "Session"
) -> schemas.Driver:
    driver = models.Driver(**driver.model_dump())
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return schemas.Driver.model_validate(driver)


async def get_all_drivers(db: "Session") -> List[schemas.Driver]:
    drivers = db.query(models.Driver).all()
    return list(map(schemas.Driver.model_validate, drivers))


async def get_driver(driver_id: int, db: "Session") -> models.Driver:
    driver = (
        db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    )
    return driver


async def delete_driver(driver: models.Driver, db: "Session"):
    db.delete(driver)
    db.commit()


async def update_driver(
    driver_data, driver: models.Driver, db: "Session"
) -> schemas.Driver:
    driver.driver_name = driver_data.driver_name
    driver.phone_number = driver_data.phone_number
    db.commit()
    db.refresh(driver)
    return schemas.Driver.model_validate(driver)


async def create_route(
    route: schemas.CreateRoute, db: "Session", driver_id, vehicle_id
) -> schemas.Route:
    route = models.Route(**route.model_dump())
    route.driver_id = driver_id
    route.vehicle_id = vehicle_id
    db.add(route)
    db.commit()
    db.refresh(route)
    return schemas.Route.model_validate(route)


async def get_all_routes(db: "Session") -> List[schemas.Route]:
    routes = db.query(models.Route).all()
    return list(map(schemas.Route.model_validate, routes))


async def get_route(route_id: int, db: "Session") -> models.Route:
    route = db.query(models.Route).filter(models.Route.id == route_id).first()
    return route


async def delete_route(route: models.Route, db: "Session"):
    db.delete(route)
    db.commit()


async def update_route(
    route_data, route: models.Route, db: "Session"
) -> schemas.Route:
    route.route_name = route_data.route_name
    route.route_info = route_data.route_info
    db.commit()
    db.refresh(route)
    return schemas.Route.model_validate(route)
