from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
import traceback

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title='RevCare API', version='1.0')

@app.middleware("http")
async def ErrorHandlerMiddleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as e:
        # Let known HTTP exceptions pass through unchanged
        raise e

    except Exception as e:
        # Log detailed error info
        error_info = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc(),
        }

        logger.error(
            f"Unhandled exception at {request.method} {request.url.path}: {e}\n{error_info['traceback']}"
        )

        # Return a safe, generic error to the client
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred. Please try again later."},
        )