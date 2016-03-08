from django.contrib import admin
from . import models

# Register your models here.
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    pass


admin.site.register(models.CustomUser, CustomUserAdmin)
