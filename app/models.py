"""
models.py
"""


# from uuid import UUID

from uuid import uuid4

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class Fleet(Base):
    __tablename__ = "fleets"
    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4
    )
    fleet_name = Column(String, index=True, nullable=False, unique=True)
    fleet_info = Column(String, nullable=True)
    phone_number = Column(String, nullable=False, unique=True)
    date_created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4
    )
    vehicle_brand = Column(String, nullable=True)
    vehicle_plate_number = Column(
        String, index=True, nullable=False, unique=True
    )
    date_created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        UUID, ForeignKey("fleets.id", ondelete="CASCADE"), nullable=False
    )


class Driver(Base):
    __tablename__ = "drivers"
    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4
    )
    driver_name = Column(String, index=True, nullable=True)
    phone_number = Column(String, index=True, nullable=False, unique=True)
    date_created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Route(Base):
    __tablename__ = "routes"
    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4
    )
    route_name = Column(String, index=True, nullable=False)
    route_info = Column(String, nullable=True)
    driver_id = Column(
        UUID, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False
    )
    vehicle_id = Column(
        UUID, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False
    )
    date_created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
