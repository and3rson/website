from django.contrib import admin
import models
from ordered_model.admin import OrderedModelAdmin


class CategoryAdmin(OrderedModelAdmin):
    list_display = ('title', 'move_up_down_links', 'order')


class ProjectAdmin(OrderedModelAdmin):
    list_display = ('title', 'move_up_down_links', 'order')


class ScreenshotAdmin(OrderedModelAdmin):
    list_display = ('title', 'move_up_down_links', 'order')


class ProviderAdmin(admin.ModelAdmin):
    pass


class LinkAdmin(OrderedModelAdmin):
    list_display = ('url', 'provider', 'move_up_down_links', 'order')


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Screenshot, ScreenshotAdmin)
admin.site.register(models.Provider, ProviderAdmin)
admin.site.register(models.Link, LinkAdmin)
