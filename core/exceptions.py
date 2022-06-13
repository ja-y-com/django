from rest_framework import status
from rest_framework.exceptions import APIException


class AuthenticationExceptions:
    class UnAuthorized(APIException):
        error_code = 110001
        status_code = status.HTTP_401_UNAUTHORIZED
        default_detail = "회원 정보를 찾을 수 없습니다"


class UserExceptions:
    class NotFoundPhoneValidKey(APIException):
        error_code = 120001
        status_code = status.HTTP_404_NOT_FOUND
        default_detail = "입력하신 인증 번호가 올바르지 않습니다"


class SecurityExceptions:
    class NotFoundPublicKey(APIException):
        error_code = 130001
        status_code = status.HTTP_404_NOT_FOUND
        default_detail = "공개키를 찾을 수 없습니다"

    class ExpiresRSAKeySet(APIException):
        error_code = 130002
        status_code = status.HTTP_403_FORBIDDEN
        default_detail = "만료된 키입니다"


class LocationExceptions:
    class NotFoundTargetPlace(APIException):
        error_code = 140001
        status_code = status.HTTP_404_NOT_FOUND
        default_detail = "목표 위치를 찾지 못했습니다"
