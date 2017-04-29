from django.shortcuts import render
from dunai.website.models import Contact
from django.core.urlresolvers import reverse
import yaml
import os
from django.conf import settings


def view_cv(request):
    f = open(os.path.join(settings.BASE_DIR, 'cv', 'cv.yaml'), 'r')
    data = f.read()
    f.close()
    cv = yaml.load(data)

    return render(request, 'dunai/cv.jade', dict(
        contacts=Contact.objects.order_by('order'),
        breadcrumbs=[
            dict(title='Andrew Dunai', url=reverse('website:index')),
            dict(title='CV', url=reverse('cv:view')),
        ],
        page='cv',
        **cv
    ))
