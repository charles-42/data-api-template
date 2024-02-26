from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from database.core import Base
from typing import Generator
from database.authentificate import User, UserCreate, create_db_user, get_password_hash, verify_password, get_user, authenticate_user, has_access, create_access_token
import pytest
from datetime import timedelta, datetime, timezone
from jose import jwt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def session() -> Generator[Session, None, None]:
    TEST_DATABASE_URL = "sqlite:///:memory:"

    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread":False},poolclass=StaticPool)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()

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


# Test case for verify_password function
def test_verify_password():
    # Hash a password
    hashed_password = get_password_hash("test_password")

    # Verify the hashed password
    assert verify_password("test_password", hashed_password)

    # Test with incorrect password
    assert not verify_password("wrong_password", hashed_password)

# Test case for get_password_hash function
def test_get_password_hash():
    # Get the hashed password
    hashed_password = get_password_hash("test_password")

    # Assert that the hashed password is not empty
    assert hashed_password

# Test case for get_user function
def test_get_user(session):
    # Assume you have a mocked session with a DBUsers object
    username = "test_user"
    db_user = get_user(username, session)

    # Assert that the returned user object is not None
    assert db_user
    # Assert that the username matches
    assert db_user.username == username

# Test case for authenticate_user function
def test_authenticate_user(session):
    # Assume you have a mocked session with a DBUsers object
    username = "test_user"
    password = "test_password"
    db_user = authenticate_user(session, username, password)

    # Assert that the authenticated user object is not None
    assert db_user
    # Assert that the username matches
    assert db_user.username == username

    # Test with incorrect password
    assert not authenticate_user(session, username, "wrong_password")

# Define a test case
def test_create_access_token():
    # Define mock data and expires_delta
    expires_delta = timedelta(minutes=30)
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = "HS256"
    data = {"sub": "test_user"}
    # Call the function to generate the token
    token = create_access_token(data, expires_delta)
    

    # Decode the token to inspect its contents
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Assert that the token was generated correctly
    assert decoded_token["sub"] == data["sub"]
    # Assert that the token contains the expected expiration time
    expected_exp = (datetime.now(timezone.utc) + expires_delta).timestamp()
    assert decoded_token["exp"] == pytest.approx(expected_exp, abs=1)  # Use pytest.approx for floating point comparison


@pytest.mark.asyncio
async def test_get_has_access(session):
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": "test_user"}, expires_delta=access_token_expires
    )
    is_auth = await has_access(access_token, session)
    assert isinstance(is_auth, bool)
    assert is_auth == True