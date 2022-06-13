import base64
import datetime
import pytz
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from django.conf import settings
from django.db import models
from encrypted_fields import fields

from core.exceptions import SecurityExceptions
from core.keys import generate_random_string


class SecurityRSAKeySetManager(models.Manager):
    def validate_public_key(self, public_key):
        """
        공개키 유효성 검사
        :param public_key:
        :return:
        """
        # 퍼블릭키 존재 여부 확인
        key_set = self.filter(public_key=public_key)

        # 1. 키셋 존재 여부 확인 - 키 사용
        if not key_set.exists():
            raise SecurityExceptions.NotFoundPublicKey

        # 키 만료 여부 확인
        now = datetime.datetime.now().astimezone(pytz.timezone("Asia/Seoul"))
        # 만료된 키들은 모두 삭제
        SecurityRSAKeySet.objects.filter(expire_at__lt=now).delete()
        key_set = key_set.filter(expire_at__gte=now)

        # 2. 키셋 존재 여부 확인 - 만료 시간 적용
        if not key_set.exists():
            raise SecurityExceptions.ExpiresRSAKeySet
        return key_set

    def encrypt_data(self, public_key, plain_text):
        """
        데이터 암호화
        :param public_key:
        :param plain_text:
        :return:
        """
        # 키 유효성 검사
        key = self.validate_public_key(public_key).first()

        public_key = RSA.importKey(key.public_key)
        encryptor = PKCS1_OAEP.new(public_key)
        encrypted_data = encryptor.encrypt(plain_text)
        encrypted_data = base64.b64encode(encrypted_data)
        return encrypted_data

    def decrypt_data(self, public_key, encrypted_base64_data):
        """
        데이터 복호화
        :param public_key:
        :param encrypted_base64_data:
        :return:
        """
        # 키 유효성 검사
        key = self.validate_public_key(public_key).first()

        private_key = RSA.importKey(key.private_key)
        encrypted_data = base64.b64decode(encrypted_base64_data)
        decrypter = PKCS1_OAEP.new(private_key)
        decrypted = decrypter.decrypt(encrypted_data)
        return decrypted.decode()

    def create_key_set(self):
        """
        키셋 생성
        :return:
        """
        # 키셋 생성
        key_pair = RSA.generate(1024, Random.new().read)
        public_key = key_pair.publickey().exportKey().decode("ascii")
        private_key = key_pair.exportKey().decode("ascii")
        now = datetime.datetime.now().astimezone(pytz.timezone("Asia/Seoul"))
        expire_at = now + datetime.timedelta(minutes=2)

        return self.create(
            public_key=public_key, private_key=private_key, expire_at=expire_at
        )


class SecurityRSAKeySet(models.Model):
    """
    RSA 암호화 키셋
    """

    _public_key = fields.EncryptedTextField(
        verbose_name="공개 키",
    )
    public_key = fields.SearchField(
        hash_key=settings.ENCRYPTION_KEY,
        encrypted_field_name="_public_key",
        verbose_name="공개 키",
    )
    private_key = fields.EncryptedTextField(
        verbose_name="비밀 키",
    )
    expire_at = models.DateTimeField(
        verbose_name="만료 시간",
        help_text="공개키 생성 후 120초 까지만 유효",
    )

    def __str__(self):
        return f"보안 RSA 키셋 - {self.public_key}"

    objects = SecurityRSAKeySetManager()

    class Meta:
        db_table = "security_rsa_key_set"
        verbose_name = "보안 RSA 키셋"
        verbose_name_plural = verbose_name


class SecurityAESKey(models.Model):
    """
    AES 암호화 키
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="사용자"
    )
    key = models.CharField(
        max_length=32, verbose_name="AES 암호화 키", default=generate_random_string
    )

    class Meta:
        db_table = "security_aes_key"
        verbose_name = "보안 AES 키"
        verbose_name_plural = verbose_name
