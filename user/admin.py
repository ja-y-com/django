from django.contrib import admin

from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fields = (
        "name",
        "phone",
    )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_admin", "last_login")
    list_filter = ("is_active", "is_admin")
    readonly_fields = ("password", "last_login")
    search_fields = ("email",)

    inlines = [UserProfileInline]

    def has_add_permission(self, request, obj=None):
        return False
