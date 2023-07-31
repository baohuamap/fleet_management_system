import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app import models
from app.config import settings
from app.database import Base, get_db
from app.main import app

username = settings.database_username
password = settings.database_password
host = settings.database_hostname
port = settings.database_port
db_name = settings.database_name

DATABASE_URL = (
    f"postgresql://{username}:{password}@{host}:{port}/{db_name}_test"
)

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autoflush=False, autocommit=False, bind=engine
)


# check lai sau moi session co drop db k
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    # run code before run test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    # run code after test finishes


@pytest.fixture
def test_fleets(session):
    fleets_data = [
        {
            "fleet_name": "Team A",
            "fleet_info": "NYC",
            "phone_number": "113",
        },
        {
            "fleet_name": "Team B",
            "fleet_info": "BKK",
            "phone_number": "114",
        },
        {
            "fleet_name": "Team C",
            "fleet_info": "HCM",
            "phone_number": "115",
        },
    ]

    def create_fleet_model(fleet):
        return models.Fleet(**fleet)

    fleets = list(map(create_fleet_model, fleets_data))

    session.add_all(fleets)
    session.commit()

    fleets = session.query(models.Fleet).all()
    return fleets
