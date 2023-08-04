from typing import Annotated, List
from uuid import UUID

from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.orm import Session

from app import database, schemas
from app.ctrl import fleets
from app.dependencies.redis import cache
from app.security.oauth2 import verify_access_token

router = APIRouter(
    prefix="/api/fleets",
    tags=["Fleets"],
    dependencies=[Depends(verify_access_token)],
)


# fleets methods
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Fleet
)
async def create_fleet(
    fleet: schemas.CreateFleet,
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        return await fleets.create(fleet=fleet, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error create fleet",
        ) from exc


@router.get("/", response_model=List[schemas.Fleet])
async def get_fleets(
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        return await fleets.get_all(redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error get all fleets",
        ) from exc


@router.get("/{fleet_id}", response_model=schemas.Fleet)
async def get_fleet(
    fleet_id: Annotated[UUID, Path(title="The ID of the fleet to get")],
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
            detail="Fleet does not exist",
        )

    return fleet


@router.delete("/{fleet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fleet(
    fleet_id: Annotated[UUID, Path(title="The ID of the fleet to delete")],
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
            detail=f"Fleet {fleet_id} does not exist",
        )

    try:
        await fleets.delete(fleet_id=fleet_id, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error delete fleet",
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{fleet_id}", response_model=schemas.Fleet)
async def update_fleet(
    fleet_id: Annotated[UUID, Path(title="The ID of the fleet to update")],
    fleet_data: schemas.CreateFleet,
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        fleet = await fleets.get(fleet_id=fleet_id, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error get fleet"
        ) from exc

    if fleet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fleet with id {fleet_id} does not exist",
        )

    try:
        return await fleets.update(
            fleet_data=fleet_data, fleet_id=fleet_id, redis=redis, db=db
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error update fleet",
        ) from exc
