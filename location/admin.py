from django.contrib import admin

from .models import Location, TargetPlace


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(TargetPlace)
class TargetPlaceAdmin(admin.ModelAdmin):
    pass
