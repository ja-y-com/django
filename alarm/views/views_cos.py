from rest_framework import viewsets, mixins, permissions

from alarm.models import AlarmStockCos
from alarm.serializers.serializers_cos import AlarmStockCosSerializer


class AlarmStockCosViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin
):
    queryset = AlarmStockCos.objects.filter(is_enabled=True)
    serializer_class = AlarmStockCosSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
