from django.conf import settings
from django.contrib import admin
from django.urls import path, include

# 기본
urlpatterns = [
    path("sentry-debug/", lambda x: 1 / 0)
]

if settings.APP_ROLE == "API":
    # OPT 사용 일시 중단
    # from django_otp.admin import OTPAdminSite
    #
    # # 장고 어드민 접속 시 OTP 추가
    # admin.site.__class__ = OTPAdminSite

    # 장고 어드민 접속 추가
    urlpatterns += [path("admin/", admin.site.urls)]

    # 앱
    urlpatterns += [
        path("v1/notification/", include("core.urls.v1.urls_v1_notification", namespace="notification")),
        path("v1/location/", include("core.urls.v1.urls_v1_location", namespace="location")),
        path("v1/alarm/", include("core.urls.v1.urls_v1_alarm", namespace="alarm")),
    ]
    # 기타
    urlpatterns += [
        # 회원 관리
        path("accounts/", include("allauth.urls")),
    ]
