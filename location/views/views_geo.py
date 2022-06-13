from rest_framework import viewsets, mixins, response
from rest_framework.decorators import action

from core.utils.utils_map import LocationUtil
from location.models import Address
from location.serializers.serializers_geo import AddressCreateSerializer


class GEOViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    queryset = Address.objects.all()
    serializer_class = AddressCreateSerializer

    def create(self, request, *args, **kwargs):
        """
        주소 생성
        """
        return super().create(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def get_geo_data(self, request, *args, **kwargs):
        """
        주소로 위경도, 우편번호 조회
        """
        address = request.data.get("address")
        lat, lng, zip_code = LocationUtil.geo_data_from_address(address=address)
        return response.Response({
            "lat": lat,
            "lng": lng,
            "zip_code": zip_code
        })
