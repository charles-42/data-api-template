from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .core import DBUsers, DBToken, NotFoundError, get_db
from typing import Annotated
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    password: str

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_db_user(user: UserCreate,  session: Session) -> DBUsers:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user.password)
    db_user = DBUsers(
            username = user.username,
            email = user.email,
            full_name = user.full_name,
            hashed_password = hashed_password 
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

def verify_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def get_user(username: str, session: Session) -> DBUsers:
    db_user = session.query(DBUsers).filter(DBUsers.username == username).first()
    if db_user is None:
        raise NotFoundError(f"User with username {username} not found.")
    return db_user

def authenticate_user(session: Session, username: str, password: str):
    db_user = get_user(username, session)
    if not db_user:
        return False
    if not verify_password(password, db_user.hashed_password):
        return False
    return db_user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def has_access(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = DBToken(username=username)
    except JWTError:
        raise credentials_exception
    db_user = get_user(username=token_data.username,session=session)
    if db_user is None:
        raise credentials_exception
    elif db_user.disabled:
         raise HTTPException(status_code=400, detail="Inactive user")
    return True

