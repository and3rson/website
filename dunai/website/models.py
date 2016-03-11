from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from django.db import models
from ordered_model.models import OrderedModel


class Category(OrderedModel):
    class Meta(OrderedModel.Meta):
        verbose_name_plural = 'Categories'

    title = models.TextField(max_length=128)
    icon = models.CharField(max_length=128)

    def __unicode__(self):
        return u'{}'.format(self.title)


class Tag(models.Model):
    title = models.CharField(max_length=128)
    bg_color = models.CharField(max_length=32)
    text_color = models.CharField(max_length=32)
    importance = models.IntegerField(default=0)

    def __unicode__(self):
        return u'{}'.format(self.title)


class Screenshot(OrderedModel):
    title = models.CharField(max_length=128, null=True, blank=True)
    file = models.ImageField(upload_to='screenshots')

    def __unicode__(self):
        return u'{}'.format(self.title)


class Provider(models.Model):
    title = models.TextField(max_length=128)
    icon = models.CharField(max_length=128)

    def __unicode__(self):
        return u'{}'.format(self.title)


class Link(OrderedModel):
    provider = models.ForeignKey('Provider')
    url = models.URLField()

    def __unicode__(self):
        return u'{}'.format(self.url)


class Project(OrderedModel):
    title = models.CharField(max_length=128)
    category = models.ForeignKey('Category', related_name='projects')
    cover = models.ImageField(upload_to='covers')
    description = models.TextField()
    tags = models.ManyToManyField('Tag')

    screenshots = models.ManyToManyField('Screenshot')
    links = models.ManyToManyField('Link')

    def get_absolute_url(self):
        return reverse('website:project', args=(self.pk,))

    def __unicode__(self):
        return u'{}'.format(self.title)


class Contact(OrderedModel):
    title = models.CharField(max_length=128)
    url = models.URLField()
    icon = models.CharField(max_length=128, null=True, blank=True)
    bg_color = models.CharField(max_length=32, null=True, blank=True)
    text_color = models.CharField(max_length=32, null=True, blank=True)
    image = models.ImageField(upload_to='contacts', null=True, blank=True)

    def __unicode__(self):
        return u'{}'.format(self.title)
