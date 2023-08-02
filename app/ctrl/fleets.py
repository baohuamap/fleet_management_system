import json
from typing import TYPE_CHECKING, List
from uuid import UUID

from fastapi.encoders import jsonable_encoder

from app import models, schemas

if TYPE_CHECKING:
    from aioredis import Redis
    from sqlalchemy.orm import Session


async def create(
    fleet: schemas.CreateFleet,
    redis: "Redis",
    db: "Session",
) -> schemas.Fleet:
    fleet = models.Fleet(**fleet.model_dump())
    db.add(fleet)
    db.commit()
    db.refresh(fleet)
    await redis.delete("fleets")
    return schemas.Fleet.model_validate(fleet)


async def get_all(
    redis: "Redis",
    db: "Session",
) -> List[models.Fleet]:
    if (cached_profile := await redis.get("fleets")) is not None:
        fleets = json.loads(cached_profile)
        return fleets
    else:
        fleets = db.query(models.Fleet).all()
        await redis.set("fleets", json.dumps(jsonable_encoder(fleets)), ex=300)
        return fleets


async def get(
    fleet_id: UUID,
    redis: "Redis",
    db: "Session",
) -> models.Fleet:
    if (cached_profile := await redis.get(f"fleet_{fleet_id}")) is not None:
        fleet = json.loads(cached_profile)
    else:
        fleet = (
            db.query(models.Fleet).filter(models.Fleet.id == fleet_id).first()
        )

        await redis.set(
            f"fleet_{fleet_id}", json.dumps(jsonable_encoder(fleet)), ex=300
        )
    return fleet


async def delete(
    fleet_id: UUID,
    redis: "Redis",
    db: "Session",
) -> None:
    fleet = db.query(models.Fleet).filter(models.Fleet.id == fleet_id).first()
    db.delete(fleet)
    db.commit()
    await redis.delete(f"fleet_{fleet_id}")
    await redis.delete("fleets")


async def update(
    fleet_data,
    fleet_id: UUID,
    redis: "Redis",
    db: "Session",
) -> schemas.Fleet:
    fleet = db.query(models.Fleet).filter(models.Fleet.id == fleet_id).first()
    if fleet is not None:
        fleet.fleet_name = fleet_data.fleet_name
        fleet.fleet_info = fleet_data.fleet_info
        fleet.phone_number = fleet_data.phone_number
    db.commit()
    db.refresh(fleet)
    await redis.delete(f"fleet_{fleet_id}")
    await redis.delete("fleets")
    return schemas.Fleet.model_validate(fleet)
