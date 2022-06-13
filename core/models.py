import os

from django.db import models


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProjectConstant(models.Model):
    key = models.CharField("상수 키", max_length=50, unique=True)
    value = models.TextField("상수 값", blank=True)

    @classmethod
    def get_constant(cls, key: str):
        """
        상수 조회
        :param key:
        :return:
        """
        obj = cls.objects.filter(key=key).first()
        if obj is None:
            # 저장된 데이터가 없는 경우 환경 변수에서 데이터 불러와 저장
            value = os.environ.get(key)
            obj = cls.objects.create(key=key, value=value)
        return obj.value

    def __str__(self):
        return f"{self.key} - {self.value}"

    class Meta:
        db_table = "project_constant"
        verbose_name = "프로젝트 상수"
        verbose_name_plural = verbose_name

