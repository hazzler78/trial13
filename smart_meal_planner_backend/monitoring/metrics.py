from prometheus_client import Counter, Histogram, Gauge
from typing import Dict, Optional

# Request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# API metrics
api_calls_total = Counter(
    'api_calls_total',
    'Total number of external API calls',
    ['service', 'operation', 'status']
)

api_call_duration_seconds = Histogram(
    'api_call_duration_seconds',
    'External API call duration in seconds',
    ['service', 'operation'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# Business metrics
active_users_total = Gauge(
    'active_users_total',
    'Total number of active users'
)

recipes_created_total = Counter(
    'recipes_created_total',
    'Total number of recipes created',
    ['user_id']
)

meal_plans_generated_total = Counter(
    'meal_plans_generated_total',
    'Total number of meal plans generated',
    ['user_id']
)

# Rate limit metrics
rate_limit_remaining = Gauge(
    'rate_limit_remaining',
    'Number of API calls remaining before rate limit',
    ['service']
)

def track_request_duration(duration: float, method: str, endpoint: str) -> None:
    """Track HTTP request duration."""
    http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)

def track_request(method: str, endpoint: str, status: int) -> None:
    """Track HTTP request."""
    http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()

def track_api_call(
    duration: float,
    service: str,
    operation: str,
    success: bool,
    rate_limit_info: Optional[Dict[str, int]] = None
) -> None:
    """Track external API call."""
    status = "success" if success else "failure"
    api_calls_total.labels(service=service, operation=operation, status=status).inc()
    api_call_duration_seconds.labels(service=service, operation=operation).observe(duration)
    
    if rate_limit_info:
        rate_limit_remaining.labels(service=service).set(rate_limit_info.get("remaining", 0))

def track_user_activity(active_users: int) -> None:
    """Track number of active users."""
    active_users_total.set(active_users)

def track_recipe_creation(user_id: str) -> None:
    """Track recipe creation."""
    recipes_created_total.labels(user_id=user_id).inc()

def track_meal_plan_generation(user_id: str) -> None:
    """Track meal plan generation."""
    meal_plans_generated_total.labels(user_id=user_id).inc() 