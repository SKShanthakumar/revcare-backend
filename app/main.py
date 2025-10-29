from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routes import router
from app.middlewares.error_handler import register_exception_handlers
from app.utilities.seed import seed_database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Running startup tasks...")
    try:
        seed_database()
        print("Startup seeding complete.")
    except Exception as e:
        print(f"Startup seeding failed: {e}")

    yield

    print("Server shutting down...")


app = FastAPI(title='RevCare API', version='1.0', lifespan=lifespan)

register_exception_handlers(app)

app.include_router(router, prefix='/api/v1')

@app.get("/")
def welcome_message():
    data = {
        "message": "Welcome to revcare API"
    }
    return JSONResponse(content=data, status_code=200)
