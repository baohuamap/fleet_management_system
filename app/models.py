"""
models.py
"""


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class Fleet(Base):
    __tablename__ = "fleets"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    fleet_name = Column(String, index=True, nullable=False, unique=True)
    fleet_info = Column(String, nullable=True)
    phone_number = Column(String, index=True, nullable=False, unique=True)
    date_created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    vehicle_brand = Column(String, nullable=True)
    vehicle_plate_number = Column(
        String, index=True, nullable=False, unique=True
    )
    date_created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("fleets.id", ondelete="CASCADE"), nullable=False
    )


class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    driver_name = Column(String, index=True, nullable=True)
    phone_number = Column(String, index=True, nullable=False, unique=True)
    date_created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    route_name = Column(String, index=True, nullable=False)
    route_info = Column(String, nullable=True)
    driver_id = Column(
        Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False
    )
    vehicle_id = Column(
        Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False
    )
    date_created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
