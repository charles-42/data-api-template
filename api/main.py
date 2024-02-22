from fastapi import FastAPI, APIRouter
from routers.customers import router as customers_router

test_router = APIRouter()

app = FastAPI()  # FastAPI(lifespan=lifespan)

app.include_router(customers_router)

@app.get("/")
def read_root():
    return "Server is running."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)