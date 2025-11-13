from fastapi import FastAPI, Request
import logging
import time

logger = logging.getLogger("uvicorn.error")

def register_logger(app: FastAPI):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """
        Middleware to log incoming requests and their responses.
        Logs method, URL path, response status, and processing time.
        """
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000  # in ms

        logger.info(
            f"{request.method} {request.url.path} "
            f"status={response.status_code} "
            f"time={process_time:.2f}ms"
        )

        return response