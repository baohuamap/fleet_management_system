from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.orm import Session

from app import database, schemas, services

router = APIRouter(prefix="/api/drivers", tags=["Drivers"])


# drivers methods
@router.post("/", response_model=schemas.Driver)
async def create_driver(
    driver: schemas.CreateDriver, db: Session = Depends(database.get_db)
):
    try:
        return await services.create_driver(driver=driver, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error create driver",
        ) from exc


@router.get("/", response_model=List[schemas.Driver])
async def get_drivers(db: Session = Depends(database.get_db)):
    try:
        return await services.get_all_drivers(db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error get all drivers",
        ) from exc


@router.get("/{driver_id}", response_model=schemas.Driver)
async def get_driver(
    driver_id: Annotated[int, Path(title="The ID of the driver to get")],
    db: Session = Depends(database.get_db),
):
    driver = await services.get_driver(driver_id=driver_id, db=db)
    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver does not exist",
        )
    return driver


@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_driver(
    driver_id: Annotated[int, Path(title="The ID of the driver to delete")],
    db: Session = Depends(database.get_db),
):
    driver = await services.get_driver(driver_id=driver_id, db=db)
    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver {driver_id} does not exist",
        )
    try:
        await services.delete_driver(driver=driver, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error delete driver",
        ) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{driver_id}", response_model=schemas.Driver)
async def update_driver(
    driver_id: Annotated[int, Path(title="The ID of the driver to update")],
    driver_data: schemas.CreateDriver,
    db: Session = Depends(database.get_db),
):
    driver = await services.get_driver(driver_id=driver_id, db=db)
    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver does not exist",
        )
    try:
        return await services.update_driver(
            driver_data=driver_data, driver=driver, db=db
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error update driver",
        ) from exc
