from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .core import DBCustomers, NotFoundError
import string
import random

class Customer(BaseModel):
    customer_id: str
    customer_unique_id: str
    customer_zip_code_prefix: str
    customer_city: str
    customer_state: str

class CustomerCreate(BaseModel):
    customer_unique_id: str
    customer_zip_code_prefix: str
    customer_city: str
    customer_state: str


class CustomerUpdate(BaseModel):
    customer_unique_id: str
    customer_zip_code_prefix: str
    customer_city: str
    customer_state: str


def read_db_one_customer(customer_id: str, session: Session) -> DBCustomers:
    db_customer = session.query(DBCustomers).filter(DBCustomers.customer_id == customer_id).first()
    if db_customer is None:
        raise NotFoundError(f"Item with id {customer_id} not found.")
    return db_customer

def read_db_customer(session: Session) -> List[DBCustomers]:
    db_customer = session.query(DBCustomers).limit(5).all()
    if db_customer is None:
        raise NotFoundError(f"Database is empty")
    return db_customer

def generate_id():
    """Generate a unique string ID."""
    length = 14
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def create_db_customer(customer: CustomerCreate, session: Session) -> DBCustomers:
    db_customer = DBCustomers(**customer.model_dump(exclude_none=True), customer_id=generate_id())
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)

    return db_customer


def update_db_customer(customer_id: str, customer: CustomerUpdate, session: Session) -> DBCustomers:
    db_customer = read_db_one_customer(customer_id, session)
    for key, value in customer.model_dump(exclude_none=True).items():
        setattr(db_customer, key, value)
    session.commit()
    session.refresh(db_customer)

    return db_customer


def delete_db_customer(customer_id: str, session: Session) -> DBCustomers:
    db_customer = read_db_one_customer(customer_id, session)
    session.delete(db_customer)
    session.commit()
    return db_customer