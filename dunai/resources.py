from django.conf import settings
from django.http import HttpResponse
from django.template import Template, Context
from django.contrib.staticfiles import finders
import os
from dunai.utils import stripped


def google_site_verification(request):
    return HttpResponse('google-site-verification: googleb23566032253319e.html', content_type='text/plain')


def robots_txt(request):
    return HttpResponse(stripped(
        '''
        User-Agent: *
        Disallow: /api/
        Disallow: /mail/
        Disallow: /accounts/
        '''),
        content_type='text/plain'
    )


def serve_static(path, content_type, render=True):
    path = finders.find(path)

    def wrapper(request):
        f = open(os.path.join(settings.BASE_DIR, path), 'r')
        data = f.read()
        f.close()
        if render:
            content = Template(data).render(
                Context(dict(request=request))
            )
        else:
            content = data

        return HttpResponse(
            content,
            content_type=content_type
        )

    return wrapper
