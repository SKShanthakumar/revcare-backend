from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import logging
import traceback

logger = logging.getLogger("uvicorn.error")

def register_exception_handlers(app: FastAPI):
    """
    Register global exception handlers for the FastAPI application.
    
    This function sets up middleware to catch and handle various exceptions:
    - HTTPException: Passed through as-is
    - IntegrityError: Database constraint violations (duplicate keys, etc.)
    - General Exception: Unhandled errors with generic error message
    
    Args:
        app: FastAPI application instance to register handlers on
    """
    @app.middleware("http")
    async def catch_exceptions_middleware(request: Request, call_next):
        """
        Middleware to catch and handle exceptions globally.
        
        Catches exceptions during request processing and returns appropriate
        JSON error responses. Logs errors for debugging while providing
        user-friendly error messages.
        
        Args:
            request: FastAPI Request object
            call_next: Next middleware/route handler in the chain
            
        Returns:
            Response: JSON response with error details or the normal response
        """
        try:
            response = await call_next(request)
            return response
        
        except HTTPException as exc:
            pass

        except IntegrityError as exc:
            # Log full details for debugging
            logger.error(f"Database Integrity Error: {exc}")

            # Return a concise, user-friendly message
            msg = "Duplicate value or constraint violation."
            if "duplicate key value violates unique constraint" in str(exc.orig):
                msg = "Record already exists with the same unique field."

            return JSONResponse(status_code=400, content={"detail": msg})

        except Exception as exc:
            logger.error(f"Unhandled error: {exc}")
            # logger.error(traceback.format_exc())

            return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred. Please try again later."})