from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    title = models.TextField(max_length=128)
    icon = models.CharField(max_length=128)


class Project(models.Model):
    title = models.CharField(max_length=128)
    category = models.ForeignKey('Category')


class Screenshot(models.Model):
    project = models.ForeignKey('Project')

    title = models.CharField(max_length=128, null=True, blank=True)
    file = models.ImageField(upload_to='screenshots')


class Provider(models.Model):
    title = models.TextField(max_length=128)
    icon = models.CharField(max_length=128)


class Link(models.Model):
    project = models.ForeignKey('Project')

    provider = models.ForeignKey('Provider')
    url = models.URLField()
