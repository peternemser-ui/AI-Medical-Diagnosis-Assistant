"""
Backend Middleware for Request Validation, Rate Limiting, and Logging
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
from collections import defaultdict
import time
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware to prevent abuse
    """

    def __init__(self, app, max_requests=60, window_seconds=60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host

        # Skip rate limiting for health check
        if request.url.path == "/health":
            return await call_next(request)

        # Clean old requests
        current_time = time.time()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < self.window_seconds
        ]

        # Check rate limit
        if len(self.requests[client_ip]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Maximum {self.max_requests} requests per {self.window_seconds} seconds.",
                    "retry_after": self.window_seconds
                }
            )

        # Record request
        self.requests[client_ip].append(current_time)

        # Process request
        response = await call_next(request)
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Structured logging middleware for all requests
    """

    async def dispatch(self, request: Request, call_next):
        request_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        start_time = time.time()

        # Log request
        logger.info(
            f"Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host,
                "user_agent": request.headers.get("user-agent", "unknown")
            }
        )

        # Process request
        try:
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Log response
            logger.info(
                f"Request completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2)
                }
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            duration = time.time() - start_time

            logger.error(
                f"Request failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                    "duration_ms": round(duration * 1000, 2)
                },
                exc_info=True
            )

            raise


class ValidationMiddleware(BaseHTTPMiddleware):
    """
    Request validation middleware
    """

    async def dispatch(self, request: Request, call_next):
        # Validate Content-Type for POST/PUT requests
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")

            if not content_type.startswith("application/json"):
                return JSONResponse(
                    status_code=415,
                    content={
                        "error": "Unsupported Media Type",
                        "message": "Content-Type must be application/json"
                    }
                )

        # Process request
        response = await call_next(request)
        return response


class CacheMiddleware:
    """
    Simple in-memory caching for expensive operations
    """

    def __init__(self, ttl_seconds=300):
        self.cache = {}
        self.ttl_seconds = ttl_seconds

    def get(self, key):
        """Get cached value"""
        if key in self.cache:
            value, timestamp = self.cache[key]

            # Check if expired
            if time.time() - timestamp < self.ttl_seconds:
                logger.debug(f"Cache hit: {key}")
                return value
            else:
                # Remove expired entry
                del self.cache[key]
                logger.debug(f"Cache expired: {key}")

        logger.debug(f"Cache miss: {key}")
        return None

    def set(self, key, value):
        """Set cache value"""
        self.cache[key] = (value, time.time())
        logger.debug(f"Cache set: {key}")

    def delete(self, key):
        """Delete cached value"""
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache deleted: {key}")

    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        logger.info("Cache cleared")

    def get_stats(self):
        """Get cache statistics"""
        current_time = time.time()
        valid_entries = sum(
            1 for _, timestamp in self.cache.values()
            if current_time - timestamp < self.ttl_seconds
        )

        return {
            "total_entries": len(self.cache),
            "valid_entries": valid_entries,
            "expired_entries": len(self.cache) - valid_entries,
            "ttl_seconds": self.ttl_seconds
        }


# Global cache instance
cache = CacheMiddleware(ttl_seconds=300)  # 5 minutes TTL


def sanitize_input(text: str, max_length=10000) -> str:
    """
    Sanitize user input to prevent injection attacks
    """
    if not text:
        return ""

    # Remove null bytes
    text = text.replace("\x00", "")

    # Limit length
    if len(text) > max_length:
        text = text[:max_length]

    # Remove dangerous characters
    text = text.strip()

    return text


def validate_medical_input(data: dict) -> tuple[bool, str]:
    """
    Validate medical diagnosis input data
    """
    required_fields = ["age", "gender", "symptoms"]

    # Check required fields
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"

    # Validate age
    try:
        age = int(data["age"])
        if age < 0 or age > 150:
            return False, "Age must be between 0 and 150"
    except ValueError:
        return False, "Age must be a number"

    # Validate symptoms
    symptoms = data["symptoms"]
    if len(symptoms) < 5:
        return False, "Symptoms description must be at least 5 characters"

    if len(symptoms) > 10000:
        return False, "Symptoms description too long (max 10000 characters)"

    return True, ""


def create_error_response(message: str, status_code: int = 400, details=None):
    """
    Create standardized error response
    """
    error_response = {
        "error": True,
        "message": message,
        "status_code": status_code,
        "timestamp": datetime.now().isoformat()
    }

    if details:
        error_response["details"] = details

    return JSONResponse(
        status_code=status_code,
        content=error_response
    )


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # CSP for API
        response.headers["Content-Security-Policy"] = "default-src 'none'"

        return response
