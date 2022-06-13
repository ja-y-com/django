from django.contrib import admin

from core.models import ProjectConstant


@admin.register(ProjectConstant)
class ProjectConstantAdmin(admin.ModelAdmin):
    pass
