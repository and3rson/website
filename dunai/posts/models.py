from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.utils.timezone import now

from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)

    def __unicode__(self):
        return u'{}'.format(self.name)


class Post(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField()
    content = models.TextField()
    cover = models.ImageField(upload_to='covers')
    date_added = models.DateTimeField(default=now)
    categories = models.ManyToManyField('Category')

    def get_absolute_url(self):
        return reverse('posts:view', args=(self.id, self.slug,))

    def __unicode__(self):
        return u'{}'.format(self.title)
