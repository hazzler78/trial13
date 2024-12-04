import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from typing import Optional
from config import get_settings

settings = get_settings()

def init_sentry(environment: Optional[str] = None) -> None:
    """Initialize Sentry SDK with FastAPI and SQLAlchemy integrations."""
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=environment or settings.ENVIRONMENT,
            integrations=[
                FastApiIntegration(
                    transaction_style="endpoint",
                    middleware_spans=True,
                ),
                SqlalchemyIntegration(),
            ],
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
            send_default_pii=False,
            before_send=before_send,
            before_breadcrumb=before_breadcrumb,
        )

def before_send(event: dict, hint: dict) -> Optional[dict]:
    """Filter sensitive information before sending to Sentry."""
    if 'request' in event and 'headers' in event['request']:
        # Remove sensitive headers
        sensitive_headers = {'authorization', 'cookie', 'x-api-key'}
        headers = event['request']['headers']
        event['request']['headers'] = {
            k: v for k, v in headers.items()
            if k.lower() not in sensitive_headers
        }
    
    # Remove sensitive data from user context
    if 'user' in event:
        user = event['user']
        if 'email' in user:
            user['email'] = '[Filtered]'
        if 'ip_address' in user:
            user['ip_address'] = '[Filtered]'
    
    return event

def before_breadcrumb(breadcrumb: dict, hint: dict) -> Optional[dict]:
    """Filter sensitive information from breadcrumbs."""
    if breadcrumb.get('category') == 'http':
        # Remove sensitive data from HTTP breadcrumbs
        if 'data' in breadcrumb:
            data = breadcrumb['data']
            if 'headers' in data:
                sensitive_headers = {'authorization', 'cookie', 'x-api-key'}
                data['headers'] = {
                    k: v for k, v in data['headers'].items()
                    if k.lower() not in sensitive_headers
                }
    
    return breadcrumb 