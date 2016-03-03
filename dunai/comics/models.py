from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now


class Comic(models.Model):
    title = models.TextField()
    slug = models.CharField(max_length=128)
    image = models.ImageField(upload_to='comics')
    comment = models.TextField()
    added_on = models.DateTimeField(default=now)

    def get_absolute_url(self):
        return reverse('comics:view', args=(self.slug,))
