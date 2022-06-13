from django.conf import settings
from twilio.rest import Client

from core.models import ProjectConstant


def call_twilio_voice(data: dict):
    """
    트윌리오 전화
    :param data:
    :return:
    """
    target = data.get("target")
    target = target if target else settings.TWILIO_DEFAULT_MY_PHONE_NUMBER
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        url=ProjectConstant.get_constant("TWILIO_CALL_ANSWER_URL"),
        to=settings.TWILIO_DEFAULT_SENDER_PHONE_NUMBER,
        from_=target,
    )
    return call.sid
