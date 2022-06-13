import requests
from django.conf import settings


class LocationUtil:
    """
    위치 관련 유틸
    """

    @classmethod
    def timezone_from_location(cls, lat, lng):
        """위/경도로 현재 타임존 적용"""
        from timezonefinder import TimezoneFinder

        tf = TimezoneFinder()
        latitude, longitude = lat, lng
        return tf.timezone_at(lat=latitude, lng=longitude)

    @classmethod
    def geo_data_from_address(cls, address):
        """주소로 위/경도, 우편번호 조회"""
        _map = MapAPI()
        map_data = _map.get_map_data(address)
        return map_data.get('lat'), map_data.get('lng'), map_data.get('zip_code')


class MapAPI:
    """
    위도, 경도, 우편번호 조회
    """

    def __init__(self):
        self.address = None  # 주소 (Write Only)
        self.lat = None  # 위도 (Read Only)
        self.lng = None  # 경도 (Read Only)
        self.zip_code = None  # 우편 번호  (Read Only)

    def _api_data_to_json_or_raise(self, url, headers):
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        raise Exception(res.content)

    def _use_google_map(self):
        """
        구글 API 사용
        """
        try:
            import googlemaps

            # 구글 지도 API 생성
            gmaps = googlemaps.Client(key=settings.GOOGLE_GEOCODE_API_KEY)
            geo_data = gmaps.geocode(self.address)
            if geo_data or len(geo_data) > 0:
                self.lat = geo_data[0]["geometry"]["location"]["lat"]
                self.lng = geo_data[0]["geometry"]["location"]["lng"]
                self.zip_code = geo_data[0]["address_components"][-1][
                    "short_name"
                ].replace("-", "")
        except Exception as ex:
            print(f"* Map API : _use_google_map > {ex}")
            self._use_daum_map()

    def _use_daum_map(self):
        """
        다음 API 사용
        구글 API 우선 호출 후 실패시
        """
        try:
            # 카카오 API 호출
            url = (
                "https://dapi.kakao.com/v2/local/search/address.json?query="
                + self.address
            )
            headers = {"Authorization": "KakaoAK " + settings.KAKAO_GEOCODE_API_KEY}
            res = self._api_data_to_json_or_raise(url, headers)
            documents = res.get("documents")
            if documents and len(documents) > 0:
                result_address = documents[0].get("road_address")
                self.lat = result_address.get("y")
                self.lng = result_address.get("x")
                self.zip_code = result_address.get("zone_no")
        except Exception as ex:
            print(f"* Map API : _use_daum_map > {ex}")
            self._use_naver_map()

    def _use_naver_map(self):
        """
        네이버 API 사용
        다음 API 우선 호출 후 실패시
        """
        try:
            # 네이버 API 호출
            url = (
                "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query="
                + self.address
            )
            headers = {
                "X-NCP-APIGW-API-KEY-ID": settings.NAVER_GEOCODE_API_ID,
                "X-NCP-APIGW-API-KEY": settings.NAVER_GEOCODE_API_PW,
            }
            res = self._api_data_to_json_or_raise(url, headers)
            if res.get("addresses") and len(res["addresses"]) > 0:
                self.lat = res["addresses"][0].get("y")
                self.lng = res["addresses"][0].get("x")
                for value in res["addresses"][0].get("addressElements"):
                    if (
                        value.get("types")
                        and len(value["types"]) > 0
                        and value["types"][0] == "POSTAL_CODE"
                    ):
                        self.zip_code = value["longName"]
                        break
        except Exception as ex:
            print(f"* Map API : _use_naver_map > {ex}")

    def _find_from_deps(self):
        """
        구글 > 네이버 > 다음 순으로 확인
        """
        # 구글 지도 우선 실행
        self._use_google_map()
        return {"lat": self.lat, "lng": self.lng, "zip_code": self.zip_code}

    def get_map_data(self, address: str):
        """
        데이터 조회
        """
        if address is None or str(address) == "":
            # 주소 정보가 없으면 None 처리
            return {"lat": None, "lng": None, "zip_code": None}

        # 주소 정보 저장
        self.address = address
        # 순차적으로 확인
        return self._find_from_deps()
