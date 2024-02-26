# data-api-template

## Purpose

The objective of this project is to provide a standard template for creating a data API. 


It includes:

- The procedure for building a SQL database (SQLite).
- The procedure for importing data.
- An API (FastAPI) with token-based authentication.
- Endpoints for performing CRUD operations on the customers table.
- Testing of the endpoints related to CRUD operations and authentication.

## Setup

1. Create virtual environement and install requierements:


```bash

python3 -m venv env

pip install -r requirements.txt

```

2. To create the Olist database, execute these two commands:

```bash
sqlite3 olist.db < database_building/create_table.sql

sqlite3 olist.db < database_building/import_table.sql 2>/dev/null
```

3. Creatre environment variables;

In the api folder, create a .env file with a SECRET_KEY variable

4. You can execute tests to make sure the setup is good:

```bash
pytest
```

5. Launch the API from the api folder:

```bash
python3 api/main.py
```

6. Use the API:

- check that the api is running from root /
- Go to /docs to use the api
- Use the "get cutomers" endpoint to test unprotected endpoint
- Create a User with a password and a username
- Authorize with the created user
- You can now use the protected endpoints

## Ressources:

- https://fastapi.tiangolo.com/tutorial/security/
- https://github.com/ArjanCodes/examples/tree/main/2023/fastapi-router
- https://github.com/ArjanCodes/examples/tree/main/2023/apitesting
