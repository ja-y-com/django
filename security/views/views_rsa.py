from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, response, status, permissions
from rest_framework.decorators import action

from ..models import SecurityRSAKeySet
from ..serializers.serializers_rsa import (
    SecurityRSAKeySetSerializer,
    SecurityDecryptUseRSAKeySerializer,
)


class SecurityRSAKeySetViewSet(viewsets.GenericViewSet):
    queryset = SecurityRSAKeySet.objects
    serializer_class = SecurityRSAKeySetSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_summary="공개키 생성",
        operation_description="데이터 암호화가 필요한 경우 공개키 요청, 암호화(RSA 256 - PKCS1 OAEP) 한 후 BASE64 인코딩 하여 전송",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                "공개키 생성완료", SecurityRSAKeySetSerializer
            )
        },
    )
    @action(methods=["POST"], detail=False)
    def request_public_key(self, request, *args, **kwargs):
        rsa_key = self.queryset.create_key_set()
        serializer = SecurityRSAKeySetSerializer(instance=rsa_key)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="데이터 복호화",
        operation_description="비밀키를 이용한 데이터 복호화 후 건보 저장",
        request_body=SecurityDecryptUseRSAKeySerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                "복호화 완료", SecurityDecryptUseRSAKeySerializer
            )
        },
    )
    @action(methods=["POST"], detail=False)
    def decrypt_data(self, request, *args, **kwargs):
        serializer = SecurityDecryptUseRSAKeySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)
