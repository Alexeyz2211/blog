from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'password')
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name',)}),
    )

