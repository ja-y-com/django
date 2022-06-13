from django.conf import settings
from django.db import models

from encrypted_fields import fields


class Location(models.Model):
    lat = fields.EncryptedCharField(
        verbose_name="위도",
        max_length=20,
        null=True,
        blank=True
    )
    lng = fields.EncryptedCharField(
        verbose_name="경도",
        max_length=20,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.lat} | {self.lng}"

    class Meta:
        db_table = "location"
        verbose_name = "위치"
        verbose_name_plural = verbose_name


class LocationHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    target_place = models.ForeignKey(
        to="TargetPlace",
        on_delete=models.CASCADE,
        verbose_name="지정된 장소"
    )
    location = models.OneToOneField(
        to=Location,
        on_delete=models.CASCADE,
        verbose_name="위치",
        related_name="target_place"
    )

    def __str__(self):
        return f"{self.target_place} - {self.location}"

    class Meta:
        db_table = "location_history"
        verbose_name = "위치 기록"
        verbose_name_plural = verbose_name


class TargetPlace(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="사용자",
        related_name="target_places"
    )
    place_name = models.CharField(
        verbose_name="지정된 장소명",
        max_length=50
    )
    accept_range = models.PositiveIntegerField(
        default=100,
        verbose_name='GPS 허용 범위',
    )

    def __str__(self):
        return self.place_name

    def enabled_range(self, lat: str, lng: str):
        """
        GPS 허용 범위 내에 속하는지 확인
        """
        from haversine import haversine

        # 현재 위치
        current_place = (float(lat), float(lng))
        # 저장 되어있는 위치
        target_place_location = self.locations.first()
        # 저장된 장소가 없는 경우
        if target_place_location is None:
            return False
        target_place = (
            float(target_place_location.location.lat),
            float(target_place_location.location.lng)
        )
        return haversine(
            current_place, target_place, unit='m'
        ) < self.accept_range

    @classmethod
    def enabled_range_all(cls, user, lat: str, lng: str):
        """
        전체 운동 장소에 대한 범위 포함 여부
        """
        target_places = list(cls.objects.filter(user=user))
        for target_place in target_places:
            if target_place.enabled_range(lat, lng):
                return target_place.id
        return None

    class Meta:
        db_table = "target_place"
        verbose_name = "지정된 장소"
        verbose_name_plural = verbose_name


class Address(models.Model):
    address = models.CharField(
        verbose_name="주소",
        max_length=255,
    )
    location = models.OneToOneField(
        to=Location,
        on_delete=models.SET_NULL,
        verbose_name="위치",
        null=True,
        blank=True
    )
    zip_code = models.CharField(
        verbose_name="우편번호",
        max_length=10,
        null=True,
        blank=True
    )

    class Meta:
        db_table = "address"
        verbose_name = "주소"
        verbose_name_plural = verbose_name
