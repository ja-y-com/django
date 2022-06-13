import base64

from rest_framework import serializers

from core.serializers import DoesntStoreSerializer
from ..models import SecurityRSAKeySet


class SecurityRSAKeySetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityRSAKeySet
        fields = (
            "public_key",
            "expire_at",
        )
        read_only_fields = ("public_key", "expire_at")


class SecurityDecryptUseRSAKeySerializer(DoesntStoreSerializer):
    # 요청 데이터
    public_key = serializers.CharField(label="공개키", write_only=True)
    encrypted_data = serializers.ListSerializer(
        label="암호화된 데이터",
        help_text="암호화된 데이터의 길이가 길어서 리스트의 형태로 받는다.",
        child=serializers.CharField(),
        write_only=True,
        allow_empty=True,
    )
    # 결과 데이터
    decrypted_data = serializers.CharField(
        label="복호화된 데이터", required=False, read_only=True, allow_null=True
    )

    def save(self, **kwargs):
        # 데이터 변환
        encrypted_strings = self.validated_data.get("encrypted_data")
        decrypted_data_list = []
        for encrypted_string in encrypted_strings:
            # 데이터 복호화
            decrypted_data_list.append(
                SecurityRSAKeySet.objects.decrypt_data(
                    public_key=self.validated_data.get("public_key"),
                    encrypted_base64_data=encrypted_string,
                )
            )
        decrypted_data = base64.b64decode("".join(decrypted_data_list))
        self.validated_data["decrypted_data"] = decrypted_data
