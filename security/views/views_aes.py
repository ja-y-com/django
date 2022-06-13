from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import viewsets, status, permissions, mixins

from security.models import SecurityAESKey
from security.serializers.serializers_aes import SecurityAESKeyGenerateSerializer


class SecurityAESKeyViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin
):
    queryset = SecurityAESKey.objects.all()
    serializer_class = SecurityAESKeyGenerateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [OAuth2Authentication]

    @swagger_auto_schema(
        operation_summary="암호키 생성",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                "공개키 생성완료", SecurityAESKeyGenerateSerializer
            )
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
