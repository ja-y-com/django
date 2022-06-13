import json

import requests
from django.core.cache import cache

from core.external_api.kakao.token import refresh_kakao_tokens
from core.models import ProjectConstant


def send_kakao_to_me(template: dict):
    """
    카카오톡 나에게 보내기
    """
    # 변수 조회
    access_token = cache.get("kakao_access_token")
    if access_token is None:
        access_token = refresh_kakao_tokens()

    # 호출
    header = {"Authorization": "Bearer " + access_token}
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    data = {"template_object": json.dumps(template)}
    res = requests.post(url, headers=header, data=data)
    return res


def send_kakao_to_friend(template: dict):
    """
    카카오톡 친구에게 보내기
    """
    # 변수 조회
    access_token = cache.get("kakao_access_token")
    if access_token is None:
        refresh_kakao_tokens()
        access_token = cache.get("kakao_access_token")

    uuid = ProjectConstant.get_constant("KAKAO_API_TALK_MY_UUID")

    # 호출
    header = {"Authorization": "Bearer " + access_token}
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    data = {"receiver_uuids": f'["{uuid}"]', "template_object": json.dumps(template)}
    res = requests.post(url, headers=header, data=data)
    return res
