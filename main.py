from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app import revare_v1
from app.middlewares.error_handler import register_exception_handlers
from app.middlewares.logging import register_logger
from app.database.mongo import close_mongo_connection
from app.database import Base, engine
from app.utilities.seed import run_seed
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Handles startup and shutdown tasks for the FastAPI application.
    Manages database connections and can run seed data initialization.
    
    Yields:
        None: Control is yielded to the application
    """
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


app = FastAPI(title='RevCare API', lifespan=lifespan, docs_url=None)

origins = ['http://localhost:5173']

# middleware registration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# custom middlewares
register_logger(app)
register_exception_handlers(app)

app.include_router(revare_v1.router, prefix='/api/v1')

@app.get("/")
async def welcome_message():
    """
    Welcome endpoint for the API.
    
    Returns:
        JSONResponse: Welcome message
    """
    data = {
        "message": "Welcome to revcare API"
    }
    return JSONResponse(content=data, status_code=200)


@app.get("/docs", include_in_schema=False)
def custom_docs():
    from app.utilities.custom_swagger import html
    return HTMLResponse(content=html)
