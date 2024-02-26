from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from database.core import Base, DBCustomers
from typing import Generator
from database.customers import CustomerCreate, create_db_customer, generate_id
from database.authentificate import UserCreate, create_db_user
import pytest
from passlib.context import CryptContext


@pytest.fixture
def session() -> Generator[Session, None, None]:
    TEST_DATABASE_URL = "sqlite:///:memory:"

    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread":False},poolclass=StaticPool)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()

    #create test customers
    db_customer = DBCustomers(
            customer_id = generate_id(),
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
    assert len(customer.customer_id) == 14
    assert customer.customer_unique_id == "861eff4711a542e4b93843c6dd7febb0"
    assert customer.customer_zip_code_prefix == "14409"
    assert customer.customer_city=="franca"
    assert customer.customer_state=="SP"


def test_create_user(session:Session) -> None: 
    user = create_db_user( 
        UserCreate( 
            username="test_user",
            email = "test_user@test.com",
            full_name="test_user_fullname",
            password = "test_password"
            ), 
            session)
    
    
    assert user.username == "test_user"
    assert user.email == "test_user@test.com"
    assert user.full_name=="test_user_fullname"
    assert user.disabled==False
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    assert pwd_context.verify("test_password", user.hashed_password)

