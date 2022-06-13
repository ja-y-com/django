from django.db import models

from encrypted_fields import fields

from core.models import TimeStampModel


class NotificationBase(TimeStampModel):
    """
    메세지 기본
    """

    target = models.CharField("대상", max_length=50, null=True, blank=True)
    message = fields.EncryptedTextField(verbose_name="내용", null=True, blank=True)

    def __str__(self):
        return f"{self.target} / {self.message[:10]}"

    class Meta:
        abstract = True


class NotificationExternalAPI(models.Model):
    """
    외부 API 상태
    """

    status_code = models.CharField("상태 코드", max_length=10)
    raw = fields.EncryptedCharField("오류 메세지", max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class NotificationSMS(NotificationBase, NotificationExternalAPI):
    """
    문자 관리
    """

    class Meta:
        db_table = "notification_sms"
        verbose_name = "문자 관리"
        verbose_name_plural = verbose_name


class NotificationEmail(NotificationBase):
    """
    이메일 관리
    """

    subject = fields.EncryptedCharField(verbose_name="제목", max_length=50)

    class Meta:
        db_table = "notification_email"
        verbose_name = "이메일 관리"
        verbose_name_plural = verbose_name


class NotificationSlack(NotificationBase, NotificationExternalAPI):
    """
    슬랙 관리
    """

    channel = models.CharField("채널", max_length=50)

    class Meta:
        db_table = "notification_slack"
        verbose_name = "슬랙 관리"
        verbose_name_plural = verbose_name


class NotificationKaKaO(NotificationBase, NotificationExternalAPI):
    """
    카카오톡 관리
    """

    class Meta:
        db_table = "notification_kakao"
        verbose_name = "카카오톡 관리"
        verbose_name_plural = verbose_name


class NotificationTwilio(NotificationBase, NotificationExternalAPI):
    """
    Twilio 관리
    """

    class Meta:
        db_table = "notification_twilio"
        verbose_name = "Twilio 관리"
        verbose_name_plural = verbose_name
