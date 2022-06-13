from rest_framework_nested import routers

from notification.views.views_send import NotificationSendViewSet

app_name = "v1_notification"

router = routers.SimpleRouter()

router.register("send", NotificationSendViewSet)

urlpatterns = router.urls
