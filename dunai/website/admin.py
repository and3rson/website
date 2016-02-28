from xml.dom.domreg import registered
from django.contrib import admin
from django import forms
# from django.contrib.admin.widgets import FilteredSelectMultiple
import models
from ordered_model.admin import OrderedModelAdmin
from pagedown.widgets import AdminPagedownWidget


class CategoryAdmin(OrderedModelAdmin):
    list_display = ('title', 'move_up_down_links', 'order')


class TagAdmin(admin.ModelAdmin):
    pass


class ProjectAdminForm(forms.ModelForm):
    description = forms.CharField(widget=AdminPagedownWidget())
    # screenshots = forms.ModelMultipleChoiceField(
    #     label='Screenshots',
    #     queryset=models.Screenshot.objects.all(),
    #     required=False
    # )
    # links = forms.ModelMultipleChoiceField(
    #     label='Links',
    #     queryset=models.Link.objects.all(),
    #     required=False
    # )

    # def __init__(self, *args, **kwargs):
    #     forms.ModelForm.__init__(self, *args, **kwargs)

    class Meta:
        exclude = ('',)
        model = models.Project


class ProjectAdmin(OrderedModelAdmin):
    # def get_form(self, request, obj=None, **kwargs):
    #     if obj:
    #         self.form.base_fields['screenshots'].initial = [o.pk for o in obj.screenshots.all()]
    #     else:
    #         self.form.base_fields['screenshots'].initial = []
    #     return super(OrderedModelAdmin, self).get_form(request, obj, **kwargs)

    form = ProjectAdminForm
    list_display = ('title', 'move_up_down_links', 'order')
    _fieldsets = (
        (
            'General',
            dict(
                fields=(
                    'title',
                    'category',
                    'cover',
                    'description',
                    'tags',
                    'screenshots',
                    'links',
                )
            )
        ),
    )


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
