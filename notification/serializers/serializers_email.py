from notification.models import NotificationEmail
from notification.serializers.base import NotificationBaseSerializer
from notification.tasks import task_send_email


class NotificationEmailSerializer(NotificationBaseSerializer):
    def save(self, **kwargs):
        # 이메일 발송
        task_send_email.delay(data=self.validated_data)

    class Meta:
        model = NotificationEmail
        fields = ("target", "subject", "message", "is_completed")
        extra_kwargs = {
            "target": {"write_only": True},
            "subject": {"write_only": True},
            "message": {"write_only": True},
        }
