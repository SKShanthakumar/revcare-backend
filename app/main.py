from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routes import router
from app.middlewares.error_handler import register_exception_handlers
from app.utilities.seed import run_seed
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Running startup tasks...")
    try:
        # await run_seed()
        print("Startup seeding complete.")
    except Exception as e:
        print(f"Startup seeding failed: {e}")

    yield

    print("Server shutting down...")


app = FastAPI(title='RevCare API', version='1.0', lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")

register_exception_handlers(app)

app.include_router(router, prefix='/api/v1')

@app.get("/")
async def welcome_message():
    data = {
        "message": "Welcome to revcare API"
    }
    return JSONResponse(content=data, status_code=200)

@app.get("/sample_page", response_class=HTMLResponse)
async def confirm_service_page(request: Request, booking_id: int):
    """Render simple payment confirmation page."""
    return templates.TemplateResponse(
        "confirm.html",
        {"request": request, "booking_id": booking_id}
    )

# # testing purpose only
# from app.database.dependencies import get_postgres_db
# from sqlalchemy.orm import Session
# from fastapi import Depends
# from app.models import User, Customer, Mechanic, Admin, Role, Permission

# @app.get("/test")
# async def test(db: Session = Depends(get_postgres_db)):
#     role = 1
#     token_scopes = db.query(Role).filter(Role.id == role).first().permissions
#     token_scopes = [p.permission for p in token_scopes]

#     return {"scopes": token_scopes}
