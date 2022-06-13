from notification.models import NotificationSlack
from notification.serializers.base import NotificationBaseSerializer
from notification.tasks import task_send_slack_to_me


class NotificationSlackToMeSerializer(NotificationBaseSerializer):
    def save(self, **kwargs):
        # 이메일 발송
        self.validated_data["target"] = ""
        task_send_slack_to_me.delay(data=self.validated_data)

    class Meta:
        model = NotificationSlack
        fields = ("channel", "message", "is_completed")
        extra_kwargs = {
            "channel": {"write_only": True},
            "message": {"write_only": True},
        }
