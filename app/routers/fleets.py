from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.orm import Session

from app import database, schemas, services

router = APIRouter(prefix="/api/fleets", tags=["Fleets"])


# fleets methods
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Fleet,
)
async def create_fleet(
    fleet: schemas.CreateFleet, db: Session = Depends(database.get_db)
):
    try:
        return await services.create_fleet(fleet=fleet, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error create fleet",
        ) from exc


@router.get("/", response_model=List[schemas.Fleet])
async def get_fleets(db: Session = Depends(database.get_db)):
    try:
        return await services.get_all_fleets(db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error get all fleets",
        ) from exc


@router.get("/{fleet_id}", response_model=schemas.Fleet)
async def get_fleet(
    fleet_id: Annotated[int, Path(title="The ID of the fleet to get")],
    db: Session = Depends(database.get_db),
):
    fleet = await services.get_fleet(fleet_id=fleet_id, db=db)
    if fleet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fleet does not exist",
        )
    return fleet


@router.delete("/{fleet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fleet(
    fleet_id: Annotated[int, Path(title="The ID of the fleet to delete")],
    db: Session = Depends(database.get_db),
):
    try:
        fleet = await services.get_fleet(fleet_id=fleet_id, db=db)
        if fleet is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fleet does not exist",
            )
        await services.delete_fleet(fleet=fleet, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error delete fleet",
        ) from exc
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


@router.put("/{fleet_id}", tags=["Fleets"], response_model=schemas.Fleet)
async def update_fleet(
    fleet_id: Annotated[int, Path(title="The ID of the fleet to update")],
    fleet_data: schemas.CreateFleet,
    db: Session = Depends(database.get_db),
):
    try:
        fleet = await services.get_fleet(fleet_id=fleet_id, db=db)
        if fleet is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fleet with id {fleet_id} does not exist",
            )
        return await services.update_fleet(
            fleet_data=fleet_data, fleet=fleet, db=db
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error update fleet",
        ) from exc
