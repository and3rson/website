from django.contrib import admin
from . import models


class ComicAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', dict(fields=(
            'title',
            'slug',
            'image',
            'comment',
            'added_on'
        ))),
    )

admin.site.register(models.Comic, ComicAdmin)
