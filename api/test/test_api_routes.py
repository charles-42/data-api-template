from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from database.core import Base, get_db
from main import app


client  = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == 'Server is running.'


def test_create_improper_customer():
    response = client.post("/customers/",json={
            "customer_unique_id":"861eff4711a542e4b93843c6dd7febb0",
            "customer_zip_code_prefix":"14409",
            "customer_city":"franca"})
    assert response.status_code == 422, response.text
