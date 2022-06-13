import requests

from django.conf import settings
from django.core.cache import cache

from core.models import ProjectConstant


def refresh_kakao_tokens():
    """
    카카오 토큰 재발급
    :return:
    """
    from notification.tasks import task_send_slack_to_me

    res = KaKaOToken().refresh_token(cache.get("kakao_refresh_token"))
    if res.status_code == 200:
        # 정상적으로 발급한 경우 적용
        access_token = res.json().get("access_token")

        # 메모리 저장
        cache.set("kakao_access_token", access_token)

        # 슬랙 전송
        task_send_slack_to_me(
            data={
                "channel": "token",
                "message": (
                    "[ 카카오 토큰 정보 ]\n\n"
                    f"- access_token : {access_token}\n"
                    f'- refresh_token : {cache.get("kakao_refresh_token")}\n'
                ),
            }
        )
        return access_token

    if res.status_code != 200 and res.json().get("error_code") in ["KOE319", "KOE322"]:
        # 토큰이 올바르지 않은 경우 토큰 적용
        cache.set(
            "kakao_refresh_token",
            ProjectConstant.get_constant("KAKAO_MESSAGE_DEFAULT_REFRESH_TOKEN"),
        )
        refresh_kakao_tokens()
    res.raise_for_status()
    return None


class KaKaOToken:
    def __init__(self):
        self.client_id = settings.KAKAO_SEND_MESSAGE_CLIENT_ID
        self.redirect_url = settings.KAKAO_SEND_MESSAGE_REDIRECT_URL
        self.code = settings.KAKAO_SEND_MESSAGE_CODE
        self.scope = settings.KAKAO_SEND_MESSAGE_SCOPE

    def create_tokens(self):
        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_url,
            "code": self.code,
        }
        res = requests.post(url, data=data)

        if res.status_code == 200:
            cache.set("kakao_access_token", res.json().get("access_token"))
            cache.set("kakao_refresh_token", res.json().get("refresh_token"))

        return res

    def refresh_token(self, refresh_token: str):
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": refresh_token,
        }

        res = requests.post("https://kauth.kakao.com/oauth/token", data=data)

        if res.status_code == 200 and res.json().get("refresh_token"):
            # 결과값에 Refresh Token 이 있는 경우 기존 토큰 갱신
            # Refresh Token 은 만료 1달 전에 갱신
            cache.set("kakao_refresh_token", res.json().get("refresh_token"))

        return res
