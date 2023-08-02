import json
from typing import TYPE_CHECKING, List
from uuid import UUID

from fastapi.encoders import jsonable_encoder

from app import models, schemas

if TYPE_CHECKING:
    from aioredis import Redis
    from sqlalchemy.orm import Session


async def create(
    vehicle: schemas.CreateVehicle,
    owner_id,
    redis: "Redis",
    db: "Session",
) -> schemas.Vehicle:
    vehicle = models.Vehicle(**vehicle.model_dump())
    vehicle.owner_id = owner_id
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    await redis.delete("vehicles")
    await redis.delete(f"vehicles_in_fleet_{owner_id}")
    return schemas.Vehicle.model_validate(vehicle)


async def get_all(
    redis: "Redis",
    db: "Session",
) -> List[models.Vehicle]:
    if (cached_profile := await redis.get("vehicles")) is not None:
        vehicles = json.loads(cached_profile)
        return vehicles
    else:
        vehicles = db.query(models.Vehicle).all()
        await redis.set(
            "vehicles", json.dumps(jsonable_encoder(vehicles)), ex=300
        )
        return vehicles


async def get_all_vehicles_in_fleet(
    fleet_id: UUID,
    redis: "Redis",
    db: "Session",
) -> List[models.Vehicle]:
    if (
        cached_profile := await redis.get(f"vehicles_in_fleet_{fleet_id}")
    ) is not None:
        vehicles = json.loads(cached_profile)
        return vehicles
    else:
        vehicles = (
            db.query(models.Vehicle)
            .filter(models.Vehicle.owner_id == fleet_id)
            .all()
        )
        await redis.set(
            f"vehicles_in_fleet_{fleet_id}",
            json.dumps(jsonable_encoder(vehicles)),
            ex=300,
        )
        return vehicles


async def get(
    vehicle_id: UUID,
    redis: "Redis",
    db: "Session",
) -> models.Vehicle:
    if (
        cached_profile := await redis.get(f"vehicle_{vehicle_id}")
    ) is not None:
        vehicle = json.loads(cached_profile)
    else:
        vehicle = (
            db.query(models.Vehicle)
            .filter(models.Vehicle.id == vehicle_id)
            .first()
        )
        await redis.set(
            f"vehicle_{vehicle_id}",
            json.dumps(jsonable_encoder(vehicle)),
            ex=300,
        )
    return vehicle


async def delete(
    vehicle_id: UUID,
    redis: "Redis",
    db: "Session",
):
    vehicle = (
        db.query(models.Vehicle)
        .filter(models.Vehicle.id == vehicle_id)
        .first()
    )
    if vehicle is not None:
        fleet_id = vehicle.owner_id
        await redis.delete(f"vehicles_in_fleet_{fleet_id}")
    db.delete(vehicle)
    db.commit()
    await redis.delete(f"vehicle_{vehicle_id}")
    await redis.delete("vehicles")


async def update(
    vehicle_data,
    vehicle_id: UUID,
    redis: "Redis",
    db: "Session",
) -> schemas.Vehicle:
    vehicle = (
        db.query(models.Vehicle)
        .filter(models.Vehicle.id == vehicle_id)
        .first()
    )
    if vehicle is not None:
        vehicle.vehicle_brand = vehicle_data.vehicle_brand
        vehicle.vehicle_plate_number = vehicle_data.vehicle_plate_number
        fleet_id = vehicle.owner_id
        await redis.delete(f"vehicles_in_fleet_{fleet_id}")
    db.commit()
    db.refresh(vehicle)
    await redis.delete(f"vehicle_{vehicle_id}")
    await redis.delete("vehicles")
    return schemas.Vehicle.model_validate(vehicle)
