from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.orm import Session

from app import database, schemas, services

router = APIRouter(prefix="/api/routes", tags=["Routes"])


# routes methods
@router.post("/", response_model=schemas.Route)
async def create_route(
    route: schemas.CreateRoute,
    driver_id: int,
    vehicle_id: int,
    db: Session = Depends(database.get_db),
):
    driver = await services.get_driver(driver_id=driver_id, db=db)
    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver {driver_id} does not exist",
        )
    vehicle = await services.get_vehicle(vehicle_id=vehicle_id, db=db)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {vehicle_id} does not exist",
        )
    try:
        return await services.create_route(
            route=route, db=db, driver_id=driver.id, vehicle_id=vehicle.id
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error create route",
        ) from exc


@router.get("/", response_model=List[schemas.Route])
async def get_routes(db: Session = Depends(database.get_db)):
    try:
        return await services.get_all_routes(db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error get all routes",
        ) from exc


@router.get("/{route_id}", response_model=schemas.Route)
async def get_route(
    route_id: Annotated[int, Path(title="The ID of the route to get")],
    db: Session = Depends(database.get_db),
):
    route = await services.get_route(route_id=route_id, db=db)
    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route does not exist",
        )
    return route


@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(
    route_id: Annotated[int, Path(title="The ID of the route to delete")],
    db: Session = Depends(database.get_db),
):
    route = await services.get_route(route_id=route_id, db=db)
    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route does not exist",
        )
    try:
        await services.delete_route(route=route, db=db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error delete route",
        ) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{route_id}", response_model=schemas.Route)
async def update_route(
    route_id: Annotated[int, Path(title="The ID of the route to update")],
    route_data: schemas.CreateRoute,
    db: Session = Depends(database.get_db),
):
    route = await services.get_route(route_id=route_id, db=db)
    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route does not exist",
        )
    try:
        return await services.update_route(
            route=route, route_data=route_data, db=db
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error update route",
        ) from exc
