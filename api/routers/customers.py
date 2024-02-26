from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from typing import List, Annotated
from database.core import NotFoundError, get_db
from database.authentificate import oauth2_scheme, has_access, User
from database.customers import Customer, CustomerCreate, CustomerUpdate, read_db_customer, read_db_one_customer, \
    create_db_customer, update_db_customer, delete_db_customer


PROTECTED = Annotated[User, Depends(has_access)]



router = APIRouter(
    prefix="/customers",
)

@router.get("/{customer_id}", response_model=Customer)
def get_one_customer(request: Request, customer_id: str, db: Session = Depends(get_db)) -> Customer:
    try:
        db_customer = read_db_one_customer(customer_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Customer(**db_customer.__dict__)

@router.get("/", response_model=List[Customer])
def get_customers(request: Request,  db: Session = Depends(get_db)) -> List[Customer]:
    try:
        db_customer = read_db_customer(db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return [Customer(**customer.__dict__) for customer in db_customer]

@router.post("/")
def create_customer(has_access: PROTECTED, request: Request, customer: CustomerCreate, db: Session = Depends(get_db)) -> Customer:
    db_customer = create_db_customer(customer, db)
    return Customer(**db_customer.__dict__)

@router.put("/{customer_id}")
def update_customer(has_access: PROTECTED, request: Request, customer_id: str, customer: CustomerUpdate, db: Session = Depends(get_db)) -> Customer:
    try:
        db_customer = update_db_customer(customer_id, customer, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Customer(**db_customer.__dict__)

@router.delete("/{customer_id}")
def delete_customer(has_access: PROTECTED, request: Request, customer_id: str, db: Session = Depends(get_db)) -> Customer:
    try:
        db_customer = delete_db_customer(customer_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Customer(**db_customer.__dict__)

