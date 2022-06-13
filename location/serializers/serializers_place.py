from rest_framework import serializers

from core.exceptions import LocationExceptions
from location.models import Location, TargetPlace, LocationHistory


class LocationCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        label="사용자",
        default=serializers.CurrentUserDefault(),
        write_only=True
    )
    lat = serializers.CharField(
        label="위도",
        write_only=True
    )
    lng = serializers.CharField(
        label="경도",
        write_only=True
    )

    def create(self, validated_data):
        # 변수 조회
        user = validated_data.get("user")
        lat = validated_data.pop("lat")
        lng = validated_data.pop("lng")
        # 범위내 포함 여부 확인
        target_place_id = TargetPlace.enabled_range_all(
            user=user,
            lat=lat,
            lng=lng
        )
        # 범위 내에 포함되어있지 않은 경우 장소를 생성해줘야 함
        if target_place_id is None:
            raise LocationExceptions.NotFoundTargetPlace
        # 위치 생성
        Location.objects.create(lat=lat, lng=lng)
        # 히스토리 생성
        target_place = TargetPlace.objects.filter(id=target_place_id).first()
        validated_data["target_place"] = target_place
        return super().create(validated_data)

    class Meta:
        model = LocationHistory
        fields = ("user", "lat", "lng", "id")


class TargetPlaceCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        label="사용자",
        default=serializers.CurrentUserDefault(),
        write_only=True
    )
    lat = serializers.CharField(
        label="위도",
        write_only=True
    )
    lng = serializers.CharField(
        label="경도",
        write_only=True
    )

    def create(self, validated_data):
        # 위치 정보 저장
        lat = validated_data.pop("lat")
        lng = validated_data.pop("lng")
        location = Location.objects.create(lat=lat, lng=lng)
        # 지정된 장소 등록
        target_place = super().create(validated_data)
        # 운동 기록 추가
        LocationHistory.objects.create(
            target_place=target_place,
            location=location
        )
        return target_place

    class Meta:
        model = TargetPlace
        fields = ("user", "place_name", "lat", "lng")
