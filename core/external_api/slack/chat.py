import requests
from django.conf import settings


def send_slack_to_me(data: dict):
    """
    슬랙 전송 - 나에게
    """
    channel = data.get("channel")
    message = data.get("message")

    # 메시지 전송
    return requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + settings.SLACK_API_TOKEN},
        data={"channel": channel, "text": message},
    )
