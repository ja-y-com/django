from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from encrypted_fields import fields

from core.models import TimeStampModel


class ChatbotFriend(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="사용자",
        null=True,
    )
    user_key = models.CharField("사용자 키", max_length=100)

    class Meta:
        db_table = "chatbot_friend"
        verbose_name = "챗봇 친구"
        verbose_name_plural = verbose_name


class ChatbotContent(TimeStampModel):
    friend = models.ForeignKey(
        ChatbotFriend, on_delete=models.CASCADE, verbose_name="챗봇 친구"
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name="컨텐츠 연결"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        db_table = "chatbot_content"
        verbose_name = "챗봇 컨텐츠"
        verbose_name_plural = verbose_name


class ChatbotContentText(TimeStampModel):
    content = fields.EncryptedTextField(verbose_name="내용", null=True)

    class Meta:
        db_table = "chatbot_content_text"
        verbose_name = "챗봇 컨텐츠 - 텍스트"
        verbose_name_plural = verbose_name
