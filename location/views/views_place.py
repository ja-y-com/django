from rest_framework import viewsets, mixins, response
from rest_framework.decorators import action

from location.models import TargetPlace
from location.serializers.serializers_place import LocationCreateSerializer, TargetPlaceCreateSerializer


class LocationViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    queryset = TargetPlace.objects.all()
    serializer_class = LocationCreateSerializer

    def create(self, request, *args, **kwargs):
        """
        위치 기록 생성
        """
        return super().create(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def target_place(self, request, *args, **kwargs):
        """
        지정된 장소 생성
        """
        self.serializer_class = TargetPlaceCreateSerializer
        return super().create(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def is_enabled_range(self, request, *args, **kwargs):
        """
        지정된 장소 포함 범위내에 왔는지 확인
        """
        user = request.user
        lat = request.data.get("lat")
        lng = request.data.gtet("lng")
        exercise_place_id = TargetPlace.enabled_range_all(user=user, lat=lat, lng=lng)
        status_code = 200 if exercise_place_id else 404
        return response.Response({"is_enabled_range": bool(exercise_place_id)}, status=status_code)
