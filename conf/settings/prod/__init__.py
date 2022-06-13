import os

APP_ROLE = os.environ.get("APP_ROLE", default="API")


if APP_ROLE == "API":
    from .prod_api import *
elif APP_ROLE == "WORKER":
    from .prod_worker import *
