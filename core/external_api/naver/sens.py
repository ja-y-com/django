import base64
import hashlib
import hmac
import time
import requests
import json

from django.conf import settings


def send_naver_sms(data: dict):
    """
    네이버 문자 발송
    """
    message = data.get("message")
    phone = data.get("target")
    phone = str(phone).replace("-", "").strip() if phone else None
    assert phone, "휴대폰 번호가 포함되어있지 않습니다."

    service_id = settings.NAVER_CLOUD_SMS_ID
    access_key = settings.NAVER_CLOUD_ACCESS_KEY
    secret_key = settings.NAVER_CLOUD_SECRET_KEY
    send_phone_number = settings.NAVER_CLOUD_SMS_SEND_PHONE_NUMBER

    url = "https://sens.apigw.ntruss.com"
    uri = "/sms/v2/services/" + service_id + "/messages"
    api_url = url + uri

    timestamp = str(int(time.time() * 1000))
    string_to_sign = "POST " + uri + "\n" + timestamp + "\n" + access_key
    signature = make_signature(string_to_sign, secret_key)

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-signature-v2": signature,
    }

    body = {
        "type": "SMS",
        "contentType": "COMM",
        "from": send_phone_number,
        "content": message,
        "messages": [{"to": phone}],
    }

    body = json.dumps(body)
    response = requests.post(api_url, headers=headers, data=body)
    response.raise_for_status()
    return response


def make_signature(string_to_sign, secret_key):
    _secret_key = bytes(secret_key, "UTF-8")
    sign_to_bytes = bytes(string_to_sign, "UTF-8")
    string_hmac = hmac.new(
        _secret_key, sign_to_bytes, digestmod=hashlib.sha256
    ).digest()
    string_base64 = base64.b64encode(string_hmac).decode("UTF-8")
    return string_base64
