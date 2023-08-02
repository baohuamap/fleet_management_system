import json
from typing import TYPE_CHECKING, List
from uuid import UUID

from fastapi.encoders import jsonable_encoder

from app import models, schemas

if TYPE_CHECKING:
    from aioredis import Redis
    from sqlalchemy.orm import Session


async def create(
    route: schemas.CreateRoute,
    driver_id,
    vehicle_id,
    redis: "Redis",
    db: "Session",
) -> schemas.Route:
    route = models.Route(**route.model_dump())
    route.driver_id = driver_id
    route.vehicle_id = vehicle_id
    db.add(route)
    db.commit()
    db.refresh(route)
    await redis.delete("routes")
    return schemas.Route.model_validate(route)


async def get_all(
    redis: "Redis",
    db: "Session",
) -> List[models.Route]:
    if (cached_profile := await redis.get("routes")) is not None:
        routes = json.loads(cached_profile)
        return routes
    else:
        routes = db.query(models.Route).all()
        await redis.set(
            "routes",
            json.dumps(jsonable_encoder(routes)),
            ex=300,
        )
        return routes


async def get(
    route_id: UUID,
    redis: "Redis",
    db: "Session",
) -> models.Route:
    if (cached_profile := await redis.get(f"route_{route_id}")) is not None:
        route = json.loads(cached_profile)
    else:
        route = (
            db.query(models.Route).filter(models.Route.id == route_id).first()
        )
        await redis.set(
            f"route_{route_id}",
            json.dumps(jsonable_encoder(route)),
            ex=300,
        )
    return route


async def delete(
    route_id: UUID,
    redis: "Redis",
    db: "Session",
):
    route = db.query(models.Route).filter(models.Route.id == route_id).first()
    db.delete(route)
    db.commit()
    await redis.delete(f"route_{route_id}")
    await redis.delete("routes")


async def update(
    route_data,
    route_id: UUID,
    redis: "Redis",
    db: "Session",
) -> schemas.Route:
    route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if route is not None:
        route.route_name = route_data.route_name
        route.route_info = route_data.route_info
    db.commit()
    db.refresh(route)
    await redis.delete(f"route_{route_id}")
    await redis.delete("routes")
    return schemas.Route.model_validate(route)
