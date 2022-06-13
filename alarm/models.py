from django.db import models

from core.fields import PhoneNumberField


class AlarmStockClient(models.Model):
    name = models.CharField(
        verbose_name="의뢰인",
        max_length=50,
        null=True,
        blank=True
    )
    phone_number = PhoneNumberField(
        verbose_name="휴대폰 번호",
        null=True,
        blank=True
    )
    email = models.EmailField(
        verbose_name="이메일 주소",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name if self.name else self.phone_number

    class Meta:
        db_table = "alarm_stock_client"
        verbose_name = "알람 의뢰인"
        verbose_name_plural = verbose_name


class AlarmStockBase(models.Model):
    url = models.URLField(
        verbose_name="제품 링크"
    )
    option = models.CharField(
        verbose_name="옵션",
        max_length=50,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class AlarmStockCos(AlarmStockBase):
    client = models.ForeignKey(
        verbose_name="의뢰인",
        to=AlarmStockClient,
        on_delete=models.CASCADE,
    )
    is_enabled = models.BooleanField(
        verbose_name="사용 여부",
        default=True
    )

    class Meta:
        db_table = "alarm_stock_cos"
        verbose_name = "재고 알람 - 코스"
        verbose_name_plural = verbose_name
