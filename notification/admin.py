from django.contrib import admin

from notification.models import (
    NotificationSMS, NotificationEmail, NotificationSlack, NotificationKaKaO, NotificationTwilio
)


@admin.register(NotificationSMS)
class NotificationSMSAdmin(admin.ModelAdmin):
    pass


@admin.register(NotificationEmail)
class NotificationEmailAdmin(admin.ModelAdmin):
    pass


@admin.register(NotificationSlack)
class NotificationSlackAdmin(admin.ModelAdmin):
    pass


@admin.register(NotificationKaKaO)
class NotificationKaKaOAdmin(admin.ModelAdmin):
    pass


@admin.register(NotificationTwilio)
class NotificationTwilioAdmin(admin.ModelAdmin):
    pass
