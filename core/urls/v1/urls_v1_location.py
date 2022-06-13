from rest_framework_nested import routers

from location.views.views_geo import GEOViewSet
from location.views.views_place import LocationViewSet

app_name = "v1_location"

router = routers.SimpleRouter()

router.register("geo", GEOViewSet)
router.register("location", LocationViewSet)

urlpatterns = router.urls
