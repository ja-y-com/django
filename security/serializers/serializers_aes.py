from rest_framework import serializers

from security.models import SecurityAESKey


class SecurityAESKeyGenerateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        request = self.context.get("request")
        user = request.user if request else None
        assert user, "로그인된 사용자 정보가 없습니다."

        aes_key_obj, _ = SecurityAESKey.objects.get_or_create(user=user)
        return aes_key_obj

    class Meta:
        model = SecurityAESKey
        fields = (
            "user",
            "key",
        )
        read_only_fields = (
            "key",
            "user",
        )
