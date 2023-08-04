from typing import Annotated, List
from uuid import UUID

from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.orm import Session

from app import database, schemas
from app.ctrl import drivers
from app.dependencies.redis import cache
from app.security.oauth2 import verify_access_token

router = APIRouter(
    prefix="/api/drivers",
    tags=["Drivers"],
    dependencies=[Depends(verify_access_token)],
)


# drivers methods
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Driver
)
async def create_driver(
    driver: schemas.CreateDriver,
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        return await drivers.create(driver=driver, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error create driver",
        ) from exc


@router.get("/", response_model=List[schemas.Driver])
async def get_drivers(
    redis: Redis = Depends(cache),
    db: Session = Depends(database.get_db),
):
    try:
        return await drivers.get_all(redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error get all drivers",
        ) from exc


@router.get("/{driver_id}", response_model=schemas.Driver)
async def get_driver(
    driver_id: Annotated[UUID, Path(title="The ID of the driver to get")],
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
            detail="Driver does not exist",
        )

    return driver


@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_driver(
    driver_id: Annotated[UUID, Path(title="The ID of the driver to delete")],
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
        await drivers.delete(driver_id=driver_id, redis=redis, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error delete driver",
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{driver_id}", response_model=schemas.Driver)
async def update_driver(
    driver_id: Annotated[UUID, Path(title="The ID of the driver to update")],
    driver_data: schemas.CreateDriver,
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
        return await drivers.update(
            driver_data=driver_data, driver_id=driver_id, redis=redis, db=db
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error update driver",
        ) from exc
