from django.contrib import admin

from alarm.models import AlarmStockCos, AlarmStockClient


@admin.register(AlarmStockClient)
class AlarmStockClientAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "email")
    search_fields = ("phone_number", "email")


@admin.register(AlarmStockCos)
class AlarmStockCosAdmin(admin.ModelAdmin):
    list_display = ("url", "option", "client")
    list_filter = ("url",)
    search_fields = ("url",)
