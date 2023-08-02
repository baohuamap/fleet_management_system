import json
from typing import TYPE_CHECKING, List
from uuid import UUID

from fastapi.encoders import jsonable_encoder

from app import models, schemas

if TYPE_CHECKING:
    from aioredis import Redis
    from sqlalchemy.orm import Session


async def create(
    driver: schemas.CreateDriver,
    redis: "Redis",
    db: "Session",
) -> schemas.Driver:
    driver = models.Driver(**driver.model_dump())
    db.add(driver)
    db.commit()
    db.refresh(driver)
    await redis.delete("drivers")
    return schemas.Driver.model_validate(driver)


async def get_all(
    redis: "Redis",
    db: "Session",
) -> List[models.Driver]:
    if (cached_profile := await redis.get("drivers")) is not None:
        drivers = json.loads(cached_profile)
        return drivers
    else:
        drivers = db.query(models.Driver).all()
        await redis.set(
            "drivers", json.dumps(jsonable_encoder(drivers)), ex=300
        )
        return drivers


async def get(
    driver_id: UUID,
    redis: "Redis",
    db: "Session",
) -> models.Driver:
    if (cached_profile := await redis.get(f"driver_{driver_id}")) is not None:
        driver = json.loads(cached_profile)
    else:
        driver = (
            db.query(models.Driver)
            .filter(models.Driver.id == driver_id)
            .first()
        )
        await redis.set(
            f"driver_{driver_id}", json.dumps(jsonable_encoder(driver)), ex=300
        )
    return driver


async def delete(
    driver_id: UUID,
    redis: "Redis",
    db: "Session",
) -> None:
    driver = (
        db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    )
    db.delete(driver)
    db.commit()
    await redis.delete(f"driver_{driver_id}")
    await redis.delete("drivers")


async def update(
    driver_data,
    driver_id: UUID,
    redis: "Redis",
    db: "Session",
) -> schemas.Driver:
    driver = (
        db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    )
    if driver is not None:
        driver.driver_name = driver_data.driver_name
        driver.phone_number = driver_data.phone_number
    db.commit()
    db.refresh(driver)
    await redis.delete(f"driver_{driver_id}")
    await redis.delete("drivers")
    return schemas.Driver.model_validate(driver)
