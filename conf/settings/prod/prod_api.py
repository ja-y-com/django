from apscheduler.schedulers.background import BackgroundScheduler
from .base import *

ALLOWED_HOSTS += [
    "ja-y.com"
]

CSRF_TRUSTED_ORIGINS = ["https://ja-y.com"]

INSTALLED_APPS += [
    "django_apscheduler"
]

# 스케쥴러
scheduler = BackgroundScheduler(

)
scheduler.start()
