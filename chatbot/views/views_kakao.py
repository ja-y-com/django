from django.conf import settings
from rest_framework import viewsets, mixins, permissions, response

from chatbot.serializers.serializers_kakao import ChatbotCreateSerializer, ChatbotListSerializer
from core.consts import KAKAO_CHAT_BOT_DEFAULT_SIMPLE_TEXT_MESSAGE
from core.paginations import DefaultPageNumberPagination
from chatbot.models import ChatbotContent


class KaKaOChatbotViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    queryset = ChatbotContent.objects.all()
    serializer_class = ChatbotCreateSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = DefaultPageNumberPagination

    @property
    def get_error_value(self):
        template = KAKAO_CHAT_BOT_DEFAULT_SIMPLE_TEXT_MESSAGE
        template["template"]["outputs"][0]["simpleText"][
            "text"
        ] = f"오류 발생 😱 관리자에게 문의해주세요 📬 {settings.DEFAULT_ADMIN_EMAIL}"
        return template

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        assert user, "사용자가 없습니다"
        return queryset.filter(friend__user=user)

    def create(self, request, *args, **kwargs):
        try:
            resp = super().create(request, *args, **kwargs)
        except Exception as ex:
            resp = response.Response(self.get_error_value)
        return resp

    def list(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAuthenticated]
        self.serializer_class = ChatbotListSerializer
        return super().list(request, *args, **kwargs)
