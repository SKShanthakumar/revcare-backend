from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
import logging
import traceback

logger = logging.getLogger("uvicorn.error")

def register_exception_handlers(app: FastAPI):
    @app.middleware("http")
    async def catch_exceptions_middleware(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        
        except HTTPException as exc:
            pass

        except IntegrityError as exc:
            # Log full details for debugging
            logger.error(f"Database Integrity Error: {exc}")
            traceback.print_exc()

            # Return a concise, user-friendly message
            msg = "Duplicate value or constraint violation."
            if "duplicate key value violates unique constraint" in str(exc.orig):
                msg = "Record already exists with the same unique field."

            raise HTTPException(status_code=400, detail=msg)

        except Exception as exc:
            logger.error(f"Unhandled error: {exc}")
            logger.error(traceback.format_exc())

            return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred. Please try again later."})