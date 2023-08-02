"""
database.py
connect to postgres database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

username = settings.database_username
password = settings.database_password
host = settings.database_hostname
port = settings.database_port
db_name = settings.database_name

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_tables():
    return Base.metadata.create_all(bind=engine)
