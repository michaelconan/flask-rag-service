import os
from datetime import timedelta

# Set secret key, expiration, cookie location, security for JWT
JWT_SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=90)
JWT_COOKIE_SECURE = True
JWT_TOKEN_LOCATION = ["cookies"]

# Redis Cache for Celery task queue
REDIS_URL = os.getenv("REDIS_URL", default="redis://redis:6379")
CELERY = {
    "broker_url": REDIS_URL,
    "result_backend": REDIS_URL,
}

# Database URL for SQLAlchemy
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    default="postgres:postgres@db:5432/postgres",
)
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://" + DATABASE_URL

SWAGGER_CONFIG = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: rule.rule.startswith('/auth') or rule.rule.startswith('/api'),
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
