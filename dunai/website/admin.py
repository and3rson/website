from django.contrib import admin
from django import forms
import models
from ordered_model.admin import OrderedModelAdmin
from pagedown.widgets import AdminPagedownWidget


class CategoryAdmin(OrderedModelAdmin):
    list_display = ('title', 'move_up_down_links', 'order')


class TagAdmin(admin.ModelAdmin):
    pass


class ProjectAdminForm(forms.ModelForm):
    description = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        exclude = ('',)
        model = models.Project


class ProjectAdmin(OrderedModelAdmin):
    form = ProjectAdminForm
    list_display = ('title', 'move_up_down_links', 'order')


class ScreenshotAdmin(OrderedModelAdmin):
    list_display = ('title', 'move_up_down_links', 'order')


class ProviderAdmin(admin.ModelAdmin):
    pass


class LinkAdmin(OrderedModelAdmin):
    list_display = ('url', 'provider', 'move_up_down_links', 'order')


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Screenshot, ScreenshotAdmin)
admin.site.register(models.Provider, ProviderAdmin)
admin.site.register(models.Link, LinkAdmin)
