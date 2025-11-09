from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.revare_v1 import router
from app.middlewares.error_handler import register_exception_handlers
from app.database.mongo import close_mongo_connection
from app.database import Base, engine
from app.utilities.seed import run_seed
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Running startup tasks...")
    try:
        # await run_seed()
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.create_all)
        print("Postgre db connected")
        print("Mongo db connected")
        
        print("Startup complete.")
    except Exception as e:
        print(f"Startup failed: {e}")

    yield

    await close_mongo_connection()
    print("Server shutting down...")


app = FastAPI(title='RevCare API', lifespan=lifespan)

register_exception_handlers(app)

app.include_router(router, prefix='/api/v1')

@app.get("/")
async def welcome_message():
    data = {
        "message": "Welcome to revcare API"
    }
    return JSONResponse(content=data, status_code=200)
