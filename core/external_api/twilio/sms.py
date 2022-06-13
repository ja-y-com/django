from django.conf import settings
from twilio.rest import Client


def send_twilio_sms(data: dict):
    """
    트윌리오 문자 발송
    """
    message = data.get("message")
    phone = data.get("target")
    phone = str(phone).replace("-", "").strip() if phone else None
    assert phone, "휴대폰 번호가 포함되어있지 않습니다."

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        messaging_service_sid=settings.TWILIO_DEFAULT_SERVICE_SID,
        body=message,
        to=f"+82{phone.strip()[1:]}",
    )
    return message.sid
