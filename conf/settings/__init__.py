import os

APP_ENVIRONMENT = os.environ.get("APP_ENVIRONMENT", default="PROD")


if APP_ENVIRONMENT == "PROD":
    from .prod import *
