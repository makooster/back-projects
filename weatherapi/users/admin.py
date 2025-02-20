from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_superuser")
    list_filter = ("role",)
    search_fields = ("username", "email")
    ordering = ("role", "username")


try:
    admin.site.register(CustomUser, CustomUserAdmin)
except admin.sites.AlreadyRegistered:
    pass  # Prevent duplicate registration error
