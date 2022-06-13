from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from encrypted_fields import fields

from core import fields as custom_fields


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    # 이메일 주소 - 고유 값
    email = models.EmailField("이메일 주소", max_length=100, unique=True)

    # 권한 정보
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # 관리자
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = "user"
        verbose_name = "사용자"
        verbose_name_plural = verbose_name


class UserProfile(models.Model):
    # 사용자
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="사용자",
        related_name="user_profile"
    )
    # 이름, 연락처 - 암호화 필드
    _name = fields.EncryptedCharField(
        max_length=20,
        verbose_name="이름",
        null=True,
        blank=True
    )
    name = fields.SearchField(
        hash_key=settings.ENCRYPTION_KEY,
        encrypted_field_name="_name",
        verbose_name="이름",
    )
    _phone = custom_fields.PhoneNumberEncryptedField(
        max_length=20,
        verbose_name="전화번호",
        null=True,
        blank=True
    )
    phone = custom_fields.PhoneNumberSearchField(
        hash_key=settings.ENCRYPTION_KEY,
        encrypted_field_name="_phone",
        verbose_name="전화번호",
    )

    class Meta:
        db_table = "user_profile"
        verbose_name = "사용자 정보"
        verbose_name_plural = verbose_name
