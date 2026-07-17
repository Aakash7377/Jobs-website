from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "role", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("role", "phone", "profile_image")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Info", {"fields": ("role", "phone", "profile_image")}),
    )


admin.site.register(User, CustomUserAdmin)