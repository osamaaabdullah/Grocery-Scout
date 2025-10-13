import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session

from backend.main import app
from backend.database import Base, get_db
from backend.models.store_product import Store, Product, Price
from backend.models.province_price import ProvincePrice
from datetime import datetime, UTC


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables once for the test session, drop them at the end."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Provide a clean session per test using rollback."""
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)
    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session):
    """FastAPI test client with overridden DB dependency."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


class SeedDataFactory:
    def __init__(self, db: Session):
        self.db = db

    def create_store(
            self,
            retailer: str,
            store_id: int = 1234,
            store_name: str = "TestStore",
            city: str = "TestCity",
            postal_code: str = "TEST12",
            store_province: str = "TS",
            latitude: float = 1234.56,
            longitude: float = 65.4321
    ) -> Store:
        store = Store(
            retailer = retailer,
            store_id = store_id,
            store_name = store_name,
            city = city,
            postal_code = postal_code,
            store_province = store_province,
            latitude = latitude,
            longitude = longitude
        )

        self.db.add(store)
        self.db.commit()
        self.db.refresh(store)
        return store

    def create_product(
        self,
        product_id: str,
        retailer: str = "TestRetailer",
        product_name: str = "Test Product",
        product_size: str = "1 unit",
        category: str = "Misc",
        product_url: str = "test.com",
        image_url: str = "test.com"
    ) -> Product:
        product = Product(
            product_id=product_id,
            retailer=retailer,
            product_name=product_name,
            product_size=product_size,
            category=category,
            product_url = product_url,
            image_url = image_url
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def create_price(
        self,
        product_id: str,
        retailer: str = "TestRetailer",
        store_id: int = 1234,
        current_price: float = 1.0,
        regular_price: float = 1.0,
        multi_save_qty: int = None,
        multi_save_price: float = None
    ) -> Price:
        price = Price(
            product_id=product_id,
            retailer=retailer,
            store_id=store_id,
            current_price=current_price,
            regular_price=regular_price,
            multi_save_qty=multi_save_qty,
            multi_save_price=multi_save_price,
            timestamp = datetime.now(UTC)
        )
        self.db.add(price)
        self.db.commit()
        self.db.refresh(price)
        return price
    
    def create_province_price(
        self,
        product_id: str,
        retailer: str = "TestRetailer",
        province: str = "TS",
        current_price: float = 1.0,
        regular_price: float = 1.0,
        price_unit: str = "$",
        unit_type: str = "kg",
        unit_price_kg: str = None,
        unit_price_lb: str = None,
        multi_save_qty: int = None,
        multi_save_price: float = None
    ) -> ProvincePrice:
        province_price = ProvincePrice(
            product_id=product_id,
            retailer=retailer,
            province = province,
            current_price=current_price,
            regular_price=regular_price,
            price_unit = price_unit,
            unit_type = unit_type,
            unit_price_kg = unit_price_kg,
            unit_price_lb = unit_price_lb,
            multi_save_qty=multi_save_qty,
            multi_save_price=multi_save_price,
            timestamp = datetime.now(UTC)
        )

        self.db.add(province_price)
        self.db.commit()
        self.db.refresh(province_price)
        return province_price


@pytest.fixture(scope="function")
def seed_data(db_session: Session):
    """Provide a factory object to create products/prices in tests."""
    return SeedDataFactory(db_session)


@pytest.fixture(scope="function", autouse=True)
def dummy_data(db_session):
    """Insert baseline dummy rows for every test automatically."""

    store = Store(
        retailer = "Metro",
        store_id = 1,
        store_name = "Test Metro",
        city = "Test City",
        postal_code = "TEST12",
        store_province = "TS",
        latitude = 23.456,
        longitude = 54.321
    )

    product_1 = Product(
        product_id="TEST01",
        retailer="Metro",
        product_name="Milk",
        product_size="1L",
        category="Dairy",
    )

    product_2 = Product(
        product_id="TEST02",
        retailer="Metro",
        product_name="Yogurt",
        product_size="1L",
        category="Yogurt",
    )

    price_1 = Price(
        product_id="TEST01",
        retailer="Metro",
        store_id=1,
        current_price=2.99,
        regular_price=3.49,
        timestamp = datetime.now(UTC)
    )

    price_2 = Price(
        product_id="TEST02",
        retailer="Metro",
        store_id=1,
        current_price=4.99,
        regular_price=5.49,
        timestamp = datetime.now(UTC)
    )

    db_session.add(store)
    db_session.add(product_1)
    db_session.add(product_2)
    db_session.add(price_1)
    db_session.add(price_2)
    db_session.commit()

    return {"product": [product_1, product_2], "price": [price_1, price_2]}
