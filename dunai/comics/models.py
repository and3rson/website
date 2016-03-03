from django.db import models
from django.utils.timezone import now


class Comic(models.Model):
    title = models.TextField()
    image = models.ImageField(upload_to='comics')
    comment = models.TextField()
    added_on = models.DateTimeField(default=now)
