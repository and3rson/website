from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from django.db import models
from ordered_model.models import OrderedModel


class Category(OrderedModel):
    class Meta(OrderedModel.Meta):
        verbose_name_plural = 'Categories'

    title = models.TextField(max_length=128)
    icon = models.CharField(max_length=128)


class Project(OrderedModel):
    title = models.CharField(max_length=128)
    category = models.ForeignKey('Category')
    cover = models.ImageField(upload_to='covers')

    def get_absolute_url(self):
        return reverse('project', args=(self.pk,))


class Screenshot(OrderedModel):
    project = models.ForeignKey('Project')

    title = models.CharField(max_length=128, null=True, blank=True)
    file = models.ImageField(upload_to='screenshots')


class Provider(models.Model):
    title = models.TextField(max_length=128)
    icon = models.CharField(max_length=128)


class Link(OrderedModel):
    project = models.ForeignKey('Project')

    provider = models.ForeignKey('Provider')
    url = models.URLField()
