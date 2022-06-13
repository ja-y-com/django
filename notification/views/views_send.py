from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action

from notification.models import NotificationEmail
from notification.serializers.serializers_email import NotificationEmailSerializer
from notification.serializers.serializers_slack import NotificationSlackToMeSerializer
from notification.serializers.serializers_sms import NotificationSMSSerializer
from notification.serializers.serializers_kakao import NotificationKaKaOSerializer


class NotificationSendViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = NotificationEmail.objects.all()
    serializer_class = NotificationEmailSerializer

    @action(methods=["POST"], detail=False)
    def email(self, request, *args, **kwargs):
        self.serializer_class = NotificationEmailSerializer
        return super().create(request, *args, **kwargs)

    @action(methods=["POST"], detail=False)
    def sms(self, request, *args, **kwargs):
        self.serializer_class = NotificationSMSSerializer
        return super().create(request, *args, **kwargs)

    @action(methods=["POST"], detail=False)
    def slack_to_me(self, request, *args, **kwargs):
        self.serializer_class = NotificationSlackToMeSerializer
        return super().create(request, *args, **kwargs)

    @action(methods=["POST"], detail=False)
    def kakao_to_me(self, request, *args, **kwargs):
        self.serializer_class = NotificationKaKaOSerializer
        return super().create(request, *args, **kwargs)

    @action(methods=["POST"], detail=False)
    def kakao_to_friend(self, request, *args, **kwargs):
        self.serializer_class = NotificationKaKaOSerializer
        return super().create(request, *args, **kwargs)
