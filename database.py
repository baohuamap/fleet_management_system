"""
database.py
connect to postgres database
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# uncomment when not use Docker
# DATABASE_URL = "postgresql://postgres:bao@localhost:1234/fleet_vehicle_db"        

# uncomment when use Docker
DATABASE_URL = "postgresql://postgres:bao@fastapi-postgres:5432/fleet_vehicle_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,
                            autocommit=False,
                            bind=engine)

Base = declarative_base()
