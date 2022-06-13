from conf.celery import app
from core.external_api.naver.sens import send_naver_sms
from core.external_api.kakao.talk import send_kakao_to_me, send_kakao_to_friend
from core.external_api.default.email import send_email
from core.external_api.slack.chat import send_slack_to_me
from core.external_api.twilio.sms import send_twilio_sms
from notification.models import (
    NotificationKaKaO,
    NotificationSMS,
    NotificationSlack,
    NotificationEmail,
)


@app.task
def task_send_email(*args, **kwargs):
    """이메일 전송"""
    send_email(*args, **kwargs)
    # 데이터 저장
    NotificationEmail.objects.create(
        target=kwargs.get("data", {}).get("target"),
        message=kwargs.get("data", {}).get("message"),
        subject=kwargs.get("data", {}).get("subject"),
    )


@app.task
def task_send_kakao_to_me(*args, **kwargs):
    """카카오 나에게 보내기"""
    res = send_kakao_to_me(*args, **kwargs)
    # 외부 API 결과 값 저장
    NotificationKaKaO.objects.create(
        target="to_me",
        message=kwargs.get("template", {}).get("text"),
        status_code=res.status_code,
        raw=res.content if res.status_code != 200 else None,
    )


@app.task
def task_send_kakao_to_friend(*args, **kwargs):
    """카카오 친구에게 보내기"""
    res = send_kakao_to_friend(*args, **kwargs)
    # 외부 API 결과 값 저장
    NotificationKaKaO.objects.create(
        target="to_friend",
        message=kwargs.get("template", {}).get("text"),
        status_code=res.status_code,
        raw=res.content if res.status_code != 200 else None,
    )


@app.task
def task_send_slack_to_me(*args, **kwargs):
    """슬랙 나에게 보내기"""
    res = send_slack_to_me(*args, **kwargs)
    # 데이터 저장
    NotificationSlack.objects.create(
        target="",
        message=kwargs.get("data", {}).get("message"),
        channel=kwargs.get("data", {}).get("channel"),
        status_code=res.status_code,
        raw=res.content if res.status_code != 200 else None,
    )


def _task_send_sms_naver(*args, **kwargs):
    """문자 전송 - 네이버"""
    res = send_naver_sms(*args, **kwargs)
    # 데이터 저장
    NotificationSMS.objects.create(
        target=kwargs.get("data", {}).get("target"),
        message=kwargs.get("data", {}).get("message"),
        status_code=res.status_code,
        raw=res.content if res.status_code != 200 else None,
    )


def _task_send_sms_twilio(*args, **kwargs):
    """문자 전송 - 트윌리오"""
    status_code = 200
    error_message = None
    try:
        send_twilio_sms(*args, **kwargs)
    except Exception as ex:
        status_code = 400
        error_message = str(ex)
    finally:
        # 데이터 저장
        NotificationSMS.objects.create(
            target=kwargs.get("data", {}).get("target"),
            message=kwargs.get("data", {}).get("message"),
            status_code=status_code,
            raw=error_message
        )


@app.task
def task_send_sms(*args, **kwargs):
    """문자 전송"""
    # _task_send_sms_naver(*args, **kwargs)
    _task_send_sms_twilio(*args, **kwargs)
