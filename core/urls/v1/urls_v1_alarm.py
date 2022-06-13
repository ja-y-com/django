from rest_framework_nested import routers

from alarm.views.views_cos import AlarmStockCosViewSet

app_name = "v1_alarm"

router = routers.SimpleRouter()

router.register("cos", AlarmStockCosViewSet)

urlpatterns = router.urls
