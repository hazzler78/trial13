import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from . import metrics
from .logger import get_logger, log_request_info

logger = get_logger(__name__)

class RequestTracingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Start timing
        start_time = time.time()
        
        # Process request
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Track metrics
            metrics.track_request(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            )
            metrics.track_request_duration(
                duration=duration,
                method=request.method,
                endpoint=request.url.path
            )
            
            # Log request info
            log_request_info(
                logger,
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration=duration,
                user_agent=request.headers.get("user-agent"),
                client_host=request.client.host if request.client else None
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            # Track failed request
            metrics.track_request(
                method=request.method,
                endpoint=request.url.path,
                status=500
            )
            metrics.track_request_duration(
                duration=duration,
                method=request.method,
                endpoint=request.url.path
            )
            
            # Log error
            logger.error(
                "request_failed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                error=str(e),
                duration=duration
            )
            raise

class ResponseTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response 