from notification.models import NotificationSMS
from notification.tasks import task_send_sms
from notification.serializers.base import NotificationBaseSerializer


class NotificationSMSSerializer(NotificationBaseSerializer):
    def save(self, **kwargs):
        # 문자 발송
        task_send_sms.delay(data=self.validated_data)

    class Meta:
        model = NotificationSMS
        fields = ("target", "message", "is_completed")
        extra_kwargs = {"target": {"write_only": True}, "message": {"write_only": True}}
