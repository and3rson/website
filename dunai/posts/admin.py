from django import forms
from redactor.widgets import RedactorEditor
from django.contrib import admin
import models


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = models.Post
        exclude = ()
        widgets = {
            'content': RedactorEditor(),
        }


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(models.Post, PostAdmin)
