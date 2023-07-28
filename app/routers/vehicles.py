from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.orm import Session

from app import database, schemas, services

router = APIRouter(prefix="/api/vehicles", tags=["Vehicles"])


# vehicles methods
@router.post("/", response_model=schemas.Vehicle)
async def create_vehicle(
    fleet_id: int,
    vehicle: schemas.CreateVehicle,
    db: Session = Depends(database.get_db),
):
    fleet = await services.get_fleet(fleet_id=fleet_id, db=db)
    if fleet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fleet with id: {fleet_id} does not exist",
        )
    try:
        return await services.create_vehicle(
            vehicle=vehicle, owner_id=fleet_id, db=db
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error create vehicle",
        ) from exc


@router.get("/", response_model=List[schemas.Vehicle])
async def get_vehicles(db: Session = Depends(database.get_db)):
    try:
        return await services.get_all_vehicles(db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error get all vehicles",
        ) from exc


@router.get(
    "/fleet/{fleet_id}",
    response_model=List[schemas.Vehicle],
)
async def get_vehicles_in_fleet(
    fleet_id: Annotated[int, Path(title="The fleet ID own the vehicle")],
    db: Session = Depends(database.get_db),
):
    fleet = await services.get_fleet(fleet_id=fleet_id, db=db)
    if fleet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fleet does not exist",
        )
    try:
        return await services.get_all_vehicles_in_fleet(
            fleet_id=fleet_id, db=db
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error get all vehicles in fleet {fleet_id}",
        ) from exc


@router.get("/{vehicle_id}", response_model=schemas.Vehicle)
async def get_vehicle(
    vehicle_id: Annotated[int, Path(title="The ID of the vehicle to get")],
    db: Session = Depends(database.get_db),
):
    vehicle = await services.get_vehicle(vehicle_id=vehicle_id, db=db)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle does not exist",
        )
    return vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle_id: Annotated[int, Path(title="The ID of the vehicle to delete")],
    db: Session = Depends(database.get_db),
):
    vehicle = await services.get_vehicle(vehicle_id=vehicle_id, db=db)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {vehicle_id} does not exist",
        )
    try:
        await services.delete_vehicle(vehicle=vehicle, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error delete vehicle",
        ) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{vehicle_id}", response_model=schemas.Vehicle)
async def update_vehicle(
    vehicle_id: Annotated[int, Path(title="The ID of the vehicle to update")],
    vehicle_data: schemas.CreateVehicle,
    db: Session = Depends(database.get_db),
):
    vehicle = await services.get_vehicle(vehicle_id=vehicle_id, db=db)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle does not exist",
        )
    try:
        return await services.update_vehicle(
            vehicle_data=vehicle_data, vehicle=vehicle, db=db
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error update vehicle",
        ) from exc
