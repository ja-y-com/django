import os

from ..base import *
from .. import APP_ENVIRONMENT

# 추가 앱
INSTALLED_APPS += [

]

# 암호화 필드
ENCRYPTION_KEY = os.environ.get("FIELD_ENCRYPTION_KEY")
FIELD_ENCRYPTION_KEYS = [
    ENCRYPTION_KEY,
]

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.environ.get("SOCIAL_ACCOUNT_GOOGLE_CLIENT_ID"),
            "secret": os.environ.get("SOCIAL_ACCOUNT_GOOGLE_SECRET"),
        }
    }
}

# 슬랙
SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")

# Sentry
SENTRY_DNS = os.environ.get("SENTRY_DNS")
if SENTRY_DNS:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DNS,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        environment=APP_ENVIRONMENT,
        request_bodies="always",
        before_send=(
            lambda e, hint: None
            if e.get("logger") and e.get("logger") == "django.security.DisallowedHost"
            else e
        ),
    )

# 네이버 클라우드
NAVER_CLOUD_SMS_ID = os.environ.get("NAVER_CLOUD_SMS_ID")
NAVER_CLOUD_SMS_SEND_PHONE_NUMBER = os.environ.get("NAVER_CLOUD_SMS_SEND_PHONE_NUMBER")
NAVER_CLOUD_ACCESS_KEY = os.environ.get("NAVER_CLOUD_ACCESS_KEY")
NAVER_CLOUD_SECRET_KEY = os.environ.get("NAVER_CLOUD_SECRET_KEY")

# 카카오
KAKAO_SEND_MESSAGE_CLIENT_ID = os.environ.get("KAKAO_SEND_MESSAGE_CLIENT_ID")
KAKAO_SEND_MESSAGE_REDIRECT_URL = os.environ.get("KAKAO_SEND_MESSAGE_REDIRECT_URL")
KAKAO_SEND_MESSAGE_CODE = os.environ.get("KAKAO_SEND_MESSAGE_CODE")
KAKAO_SEND_MESSAGE_SCOPE = os.environ.get("KAKAO_SEND_MESSAGE_SCOPE")

# Twilio
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_DEFAULT_SERVICE_SID = os.environ.get("TWILIO_DEFAULT_SERVICE_SID")
TWILIO_DEFAULT_SENDER_PHONE_NUMBER = os.environ.get(
    "TWILIO_DEFAULT_SENDER_PHONE_NUMBER"
)
TWILIO_DEFAULT_SENDER_PHONE_NUMBER_SID = os.environ.get(
    "TWILIO_DEFAULT_SENDER_PHONE_NUMBER_SID"
)
TWILIO_DEFAULT_MY_PHONE_NUMBER = os.environ.get("TWILIO_DEFAULT_MY_PHONE_NUMBER")

# 샐러리
CELERY_TIMEZONE = TIME_ZONE
RABBITMQ_DEFAULT_USER = os.environ.get("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.environ.get("RABBITMQ_DEFAULT_PASS")
RABBITMQ_DEFAULT_VHOST = os.environ.get("RABBITMQ_DEFAULT_VHOST")
CELERY_BROKER_URL = f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@cache:5672/{RABBITMQ_DEFAULT_VHOST}"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# 지도
GOOGLE_GEOCODE_API_KEY = os.environ.get("GOOGLE_GEOCODE_API_KEY")
NAVER_GEOCODE_API_ID = os.environ.get("NAVER_GEOCODE_API_ID")
NAVER_GEOCODE_API_PW = os.environ.get("NAVER_GEOCODE_API_PW")
KAKAO_GEOCODE_API_KEY = os.environ.get("KAKAO_GEOCODE_API_KEY")