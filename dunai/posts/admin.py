from django import forms
from redactor.widgets import RedactorEditor
from django.contrib import admin
from dunai.libs.telegramchannel import TelegramChannel
from django.conf import settings
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
    actions = ['notify_to_telegram']

    def notify_to_telegram(self, request, queryset):
        channel = TelegramChannel(settings.TELEGRAM_TOKEN, settings.TELEGRAM_CHANNEL_ID)
        for post in queryset.order_by('date_added'):
            # TODO: Move this hard-coded URL to settings.
            channel.notify_text(link='http://dun.ai' + post.get_absolute_url())

    notify_to_telegram.short_description = 'Notify to Telegram'


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Category, CategoryAdmin)
