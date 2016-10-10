from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.utils.timezone import now

from django.db import models
# from django.db.models.query import QuerySet


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)

    def __unicode__(self):
        return u'{}'.format(self.name)


class Post(models.Model):
    # class PostManager(QuerySet):
    #     def _fetch_all(self):
    #         if self._result_cache is None:
    #             # Not cached
    #             pass
    #         super(self.__class__, self)._fetch_all()

    #         ids_to_update = []

    #         for result in self._result_cache:
    #             ids_to_update.append(result.id)

    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    cover = models.ImageField(upload_to='covers')
    date_added = models.DateTimeField(default=now)
    categories = models.ManyToManyField('Category')
    views = models.PositiveIntegerField(default=0)
    # likes = models.PositiveIntegerField(default=0)

    # objects = PostManager.as_manager()

    def get_absolute_url(self):
        return reverse('posts:view', args=(self.slug,))

    def __unicode__(self):
        return u'{}'.format(self.title)

    def add_view(self, ip):
        kwargs = dict(post=self, ip=ip)
        post_view = PostView.objects.filter(**kwargs).first()
        print 'get'
        if not post_view:
            print 'first!'
            self.views += 1
            PostView.objects.create(**kwargs)


class PostView(models.Model):
    post = models.ForeignKey('Post', null=False, blank=False, related_name='postview_set')
    ip = models.GenericIPAddressField(null=False, blank=False)
    date = models.DateTimeField(default=now)
