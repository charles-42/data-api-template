from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from database.core import Base, get_db, DBCustomers
from database.authentificate import create_db_user, UserCreate
from database.customers import generate_id
from main import app
from typing import Generator
import pytest 
from unittest.mock import MagicMock

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread":False},poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session() -> Generator[Session, None, None]:

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

    #create test user
    create_db_user( 
        UserCreate( 
            username="test_user",
            email = "test_user@test.com",
            full_name="test_user_fullname",
            password = "test_password"
            ), 
            db_session)

    yield db_session

    db_session.close()
    Base.metadata.drop_all(bind=engine)

# Define a pytest fixture to mock the dependencies
@pytest.fixture(autouse=False)
def valid_token(monkeypatch):
    # Mock the jwt.decode function to return the mock payload
    monkeypatch.setattr("jose.jwt.decode", MagicMock(return_value={"sub": "test_user"}))



client  = TestClient(app)


# Dependency to override the get_db dependency in the main app
def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()


app.dependency_overrides[get_db] = override_get_db

def test_read_root(session:Session):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == 'Server is running.'

def test_create_customer_unauthorize(session:Session):
    response = client.post("/customers/",json={
            "customer_unique_id":"861eff4711a542e4b93843c6dd7febb0",
            "customer_zip_code_prefix":"14409",
            "customer_city":"franca"})
    assert response.status_code == 401, response.text


def test_create_improper_customer(session:Session, valid_token):
    response = client.post("/customers/",json={
            "customer_unique_id":"861eff4711a542e4b93843c6dd7febb0",
            "customer_zip_code_prefix":"14409",
            "customer_city":"franca"}, headers={"Authorization": f"Bearer {'mocked_token'}"})
    assert response.status_code == 422, response.text


def test_create_customer(session:Session, valid_token):
    response = client.post("/customers/",json={
            "customer_unique_id":"861eff4711a542e4b93843c6dd7febb0",
            "customer_zip_code_prefix":"14409",
            "customer_city":"franca",
            "customer_state":"SP"
            }, headers={"Authorization": f"Bearer {'mocked_token'}"})
    assert response.status_code == 200, response.text

####  Authentification

def test_create_user(session:Session):
    response = client.post("/auth/create_user",json={
            "username":"test_user_2",
            "email" : "test_user@test.com",
            "full_name":"test_user_fullname",
            "password" : "test_password"
            })
    assert response.status_code == 200, response.text
    assert 'username' in response.json() 


def test_login_for_access_token(session):


    # Make a request to the endpoint
    response = client.post(
        "/auth/token",
        data={"username": "test_user", "password": "test_password"}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Assert that the response contains the access token
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"




# Define a test case
def test_is_authorized(session:Session, valid_token): 

    # Make a request to the endpoint with the mock token
    response = client.get("/auth/is_authorized/", headers={"Authorization": f"Bearer {'mocked_token'}"})
    
    # Assert the response status code
    assert response.status_code == 200
    
    # Assert any other aspects of the response if needed
    # For example, if you expect the response to contain user data
    assert response.json() == True