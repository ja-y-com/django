from rest_framework import serializers

from alarm.models import AlarmStockCos, AlarmStockClient


class AlarmStockClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmStockClient
        fields = ["name", "phone_number", "email"]


class AlarmStockCosSerializer(serializers.ModelSerializer):
    client = AlarmStockClientSerializer(
        label="의뢰인"
    )

    class Meta:
        model = AlarmStockCos
        fields = ["url", "option", "client", "id"]
