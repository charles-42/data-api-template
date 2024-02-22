from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from database.core import Base, DBCustomers
from typing import Generator
from database.customers import Customer, CustomerCreate, CustomerUpdate, read_db_customer, read_db_one_customer, \
    create_db_customer, update_db_customer, delete_db_customer
import pytest


# # Dependency to get the database session
# def override_get_db():
#     database = TesttingSessionLocal()
#     try:
#         yield database
#     finally:
#         database.close()

# app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def session() -> Generator[Session, None, None]:
    DATABASE_URL = "sqlite:///:memory:"

    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread":False},poolclass=StaticPool)
    TesttingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db_session = TesttingSessionLocal()

    #create test customers
    db_customer = DBCustomers(
            customer_id = "1234",
            customer_unique_id = "4321",
            customer_zip_code_prefix = "59000",
            customer_city="Lille",
            customer_state="HDF")
    db_session.add(db_customer)
    db_session.commit()

    yield db_session

    db_session.close()
    Base.metadata.drop_all(bind=engine)


def test_create_customers(session:Session) -> None: 
    customer = create_db_customer( 
        CustomerCreate( 
            customer_unique_id="861eff4711a542e4b93843c6dd7febb0",
            customer_zip_code_prefix = "14409",
            customer_city="franca",
            customer_state="SP"
            ), 
            session)
    assert customer.customer_unique_id == "861eff4711a542e4b93843c6dd7febb0"
    assert customer.customer_zip_code_prefix == "14409"
    assert customer.customer_city=="franca"
    assert customer.customer_state=="SP"

####....