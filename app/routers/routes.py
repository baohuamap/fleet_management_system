from typing import Annotated, List
from uuid import UUID

from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.orm import Session

from app import database, schemas
from app.ctrl import drivers, routes, vehicles
from app.dependencies.redis import cache

router = APIRouter(prefix="/api/routes", tags=["Routes"])


# routes methods
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Route,
)
async def create_route(
    route: schemas.CreateRoute,
    driver_id: UUID,
    vehicle_id: UUID,
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        driver = await drivers.get(driver_id=driver_id, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error get driver",
        ) from exc

    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver {driver_id} does not exist",
        )

    try:
        vehicle = await vehicles.get(vehicle_id=vehicle_id, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error get vehicle",
        ) from exc

    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {vehicle_id} does not exist",
        )

    try:
        return await routes.create(
            route=route,
            redis=redis,
            db=db,
            driver_id=driver.id,
            vehicle_id=vehicle.id,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error create route",
        ) from exc


@router.get("/", response_model=List[schemas.Route])
async def get_routes(
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        return await routes.get_all(redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error get all routes",
        ) from exc


@router.get("/{route_id}", response_model=schemas.Route)
async def get_route(
    route_id: Annotated[UUID, Path(title="The ID of the route to get")],
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        route = await routes.get(route_id=route_id, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error get route",
        ) from exc

    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route does not exist",
        )

    return route


@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(
    route_id: Annotated[UUID, Path(title="The ID of the route to delete")],
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        route = await routes.get(route_id=route_id, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error get route",
        ) from exc

    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route {route_id} does not exist",
        )

    try:
        await routes.delete(route_id=route_id, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error delete route",
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{route_id}", response_model=schemas.Route)
async def update_route(
    route_id: Annotated[UUID, Path(title="The ID of the route to update")],
    route_data: schemas.CreateRoute,
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        route = await routes.get(route_id=route_id, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error get route",
        ) from exc

    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route does not exist",
        )

    try:
        return await routes.update(
            route_id=route_id, route_data=route_data, redis=redis, db=db
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error update route",
        ) from exc
