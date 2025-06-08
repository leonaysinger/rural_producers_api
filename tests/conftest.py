import os
from decimal import Decimal
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from alembic import command
from alembic.config import Config
from app.core.dependencies import get_db
from app.db.base import Base
from app.domain.models.rural_property import RuralProperty
from app.domain.schemas.rural_property import RuralPropertyCreate
from app.main import app
from faker import Faker
from tests.mocks import mock_user

os.environ["TESTING"] = "true"
TEST_DATABASE_URL = "postgresql://test_user:test_pass@localhost:5433/test_db"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

fake = Faker('pt_BR')


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """Aplica as migrations no banco de testes antes de qualquer teste."""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

    yield


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db
    yield TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def clean_tables_once():
    with engine.connect() as conn:
        trans = conn.begin()
        tables = ", ".join([table.name for table in Base.metadata.sorted_tables])
        conn.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE;"))
        trans.commit()
    yield


@pytest.fixture
def mock_user_model():
    return mock_user()


@pytest.fixture
def valid_cpf():
    return '482.163.270-56'

@pytest.fixture
def invalid_cpf():
    return '481.162.270-56'

@pytest.fixture
def valid_cnpj():
    return '72.249.686/0001-60'

@pytest.fixture
def invalid_cnpj():
    return '72.249.622/0001-60'

@pytest.fixture
def rural_property_mock():
    return RuralPropertyCreate(name="Test",
                               city="Florianópolis",
                               state="SC",
                               cep="00000000",
                               number="21",
                               producer_id = uuid4(),
                               description="test",
                               total_area=Decimal("2000.0"),
                               farming_area=Decimal("1000"),
                               vegetation_area=Decimal("1000"),
                               crops=[])

@pytest.fixture
def rural_property_1():
    return RuralProperty(name="Fazenda 1")

@pytest.fixture
def seed_data_extended(client: TestClient):
    producers = []
    for i in range(3):
        res = client.post("/api/producers", json={
            "name": f"Produtor {i + 1}",
            "document_type": "CPF",
            "document": fake.unique.cpf()
        })
        producers.append(res.json())

    crops = []
    for name in ["Cevada", "Tomate", "batata"]:
        res = client.post("/api/crops", json={"name": name})
        crops.append(res.json())

    seasons = []
    for year in [2024, 2025]:
        res = client.post("/api/seasons", json={"name": f"Safra {year} - teste", "year": year})
        seasons.append(res.json())

    properties = []

    payloads = [
        {
            "producer_id": producers[0]["id"],
            "name": "Fazenda Goiás",
            "city": "Luziânia",
            "state": "GO",
            "cep": "72800-000",
            "number": "123",
            "description": "Plantação de soja",
            "total_area": 100.0,
            "farming_area": 70.0,
            "vegetation_area": 30.0,
            "property_crops": [
                {"season_id": seasons[0]["id"], "crop_id": crops[0]["id"]}
            ]
        },
        {
            "producer_id": producers[1]["id"],
            "name": "Sítio São Paulo",
            "city": "Campinas",
            "state": "SP",
            "cep": "13000-000",
            "number": "456",
            "description": "Milho e algodão",
            "total_area": 200.0,
            "farming_area": 150.0,
            "vegetation_area": 50.0,
            "property_crops": [
                {"season_id": seasons[1]["id"], "crop_id": crops[1]["id"]},
                {"season_id": seasons[1]["id"], "crop_id": crops[2]["id"]}
            ]
        },
        {
            "producer_id": producers[2]["id"],
            "name": "Chácara MG",
            "city": "Uberlândia",
            "state": "MG",
            "cep": "38400-000",
            "number": "789",
            "description": "Diversificada",
            "total_area": 120.0,
            "farming_area": 90.0,
            "vegetation_area": 30.0,
            "property_crops": [
                {"season_id": seasons[0]["id"], "crop_id": crops[0]["id"]},
                {"season_id": seasons[1]["id"], "crop_id": crops[1]["id"]}
            ]
        }
    ]

    for data in payloads:
        res = client.post("/api/properties", json=data)
        properties.append(res.json())

    return {
        "producers": producers,
        "crops": crops,
        "seasons": seasons,
        "properties": properties
    }