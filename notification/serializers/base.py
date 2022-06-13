from rest_framework import serializers


class NotificationBaseSerializer(serializers.ModelSerializer):
    is_completed = serializers.BooleanField(label="전송 여부", read_only=True, default=True)
