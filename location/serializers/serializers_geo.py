from rest_framework import serializers

from core.utils.utils_map import LocationUtil
from location.models import Address, Location


class AddressCreateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        address = self.validated_data.get("address")
        lat, lng, zip_code = LocationUtil.geo_data_from_address(address=address)
        location = Location.objects.create(
            lat=lat,
            lng=lng
        )
        self.validated_data["location"] = location
        self.validated_data["zip_code"] = zip_code
        return super().save(**kwargs)

    class Meta:
        model = Address
        fields = ["address", "location", "zip_code"]
        read_only_fields = ["location", "zip_code"]
