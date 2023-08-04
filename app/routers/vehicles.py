from typing import Annotated, List
from uuid import UUID

from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.orm import Session

from app import database, schemas
from app.ctrl import fleets, vehicles
from app.dependencies.redis import cache
from app.security.oauth2 import verify_access_token

router = APIRouter(
    prefix="/api/vehicles",
    tags=["Vehicles"],
    dependencies=[Depends(verify_access_token)],
)


# vehicles methods
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Vehicle
)
async def create_vehicle(
    vehicle: schemas.CreateVehicle,
    fleet_id: UUID,
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        fleet = await fleets.get(fleet_id=fleet_id, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error get fleet",
        ) from exc

    if fleet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fleet with id: {fleet_id} does not exist",
        )

    try:
        return await vehicles.create(
            vehicle=vehicle, owner_id=fleet_id, redis=redis, db=db
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error create vehicle",
        ) from exc


@router.get("/", response_model=List[schemas.Vehicle])
async def get_vehicles(
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        return await vehicles.get_all(redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error get all vehicles",
        ) from exc


@router.get("/fleet/{fleet_id}", response_model=List[schemas.Vehicle])
async def get_vehicles_in_fleet(
    fleet_id: Annotated[UUID, Path(title="The fleet ID own the vehicle")],
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        fleet = await fleets.get(fleet_id=fleet_id, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error get fleet {fleet_id}",
        ) from exc

    if fleet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fleet does not exist",
        )

    try:
        return await vehicles.get_all_vehicles_in_fleet(
            fleet_id=fleet_id, redis=redis, db=db
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error get all vehicles in fleet {fleet_id}",
        ) from exc


@router.get("/{vehicle_id}", response_model=schemas.Vehicle)
async def get_vehicle(
    vehicle_id: Annotated[UUID, Path(title="The ID of the vehicle to get")],
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
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
            detail="Vehicle does not exist",
        )

    return vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle_id: Annotated[UUID, Path(title="The ID of the vehicle to delete")],
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
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
        await vehicles.delete(vehicle_id=vehicle_id, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error delete vehicle",
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{vehicle_id}", response_model=schemas.Vehicle)
async def update_vehicle(
    vehicle_id: Annotated[UUID, Path(title="The ID of the vehicle to update")],
    vehicle_data: schemas.CreateVehicle,
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
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
            detail="Vehicle does not exist",
        )

    try:
        return await vehicles.update(
            vehicle_data=vehicle_data,
            vehicle_id=vehicle_id,
            redis=redis,
            db=db,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error update vehicle",
        ) from exc
