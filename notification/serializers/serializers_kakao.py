from core.consts import KAKAO_CHAT_BOT_DEFAULT_SIMPLE_TEXT_MESSAGE_FORMAT
from notification.models import NotificationKaKaO
from notification.serializers.base import NotificationBaseSerializer
from notification.tasks import task_send_kakao_to_friend, task_send_kakao_to_me


class NotificationKaKaOSerializer(NotificationBaseSerializer):
    def save(self, **kwargs):
        # 메시지 변환
        message = self.validated_data.get("message")
        template = KAKAO_CHAT_BOT_DEFAULT_SIMPLE_TEXT_MESSAGE_FORMAT
        template["text"] = message

        # 카카오톡 발송
        if self.validated_data.get("target") == "to_me":
            task_send_kakao_to_me.delay(template=template)
        else:
            task_send_kakao_to_friend.delay(template=template)

    class Meta:
        model = NotificationKaKaO
        fields = ("target", "message", "is_completed")
        extra_kwargs = {"target": {"write_only": True}, "message": {"write_only": True}}
