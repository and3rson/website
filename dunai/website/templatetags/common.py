# -*- coding: utf-8 -*-
from base64 import b64encode
import hashlib
from json import dumps
import re
import urllib2
from django.conf import settings
from StringIO import StringIO
# import cssmin
from django.contrib.staticfiles import finders
from django.core.urlresolvers import resolve, Resolver404
from django.template import Library
import os
from django.templatetags.static import static
from django.utils.html import strip_tags as strip_tags_original
from django.utils.safestring import mark_safe
from django.utils.translation import get_language_from_request
import math
# import jsmin
from time import time
from django.conf import settings
from django import template
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.utils import translation
from PIL import Image, ImageFilter
from django.db.models.fields.files import ImageFieldFile
from babel.dates import format_timedelta
from django.utils.timezone import now
import re
import pydot
from HTMLParser import HTMLParser
import hashlib
from xml.dom import minidom
from bs4 import BeautifulSoup as BS
from bs4.element import Tag

register = Library()


@register.filter()
def human_readable(value):
    try:
        value = int(value)
    except:
        return value

    if value < 1000:
        return value
    elif value < 1000000:
        value /= 100

        if value % 10 == 0:
            return '{}k'.format(value / 10)
        else:
            return '{}k'.format(value / 10.0)
    else:
        value /= 100000

        if value % 10 == 0:
            return '{}m'.format(value / 10)
        else:
            return '{}m'.format(value / 10.0)


@register.simple_tag()
def load_template(id_, path):
    f = open(os.path.join(settings.BASE_DIR, path), 'r')
    src = f.read()
    f.close()

    return '<script type="text/template" id="{}">\n{}\n</script>'.format(id_, src)

ICON = '<i class="zmdi zmdi-hc-1_5x {}"></i>'


@register.simple_tag()
def star_rating(current, maximum):
    stars = []
    current = float(current)
    for i in xrange(0, maximum):
        diff = current - i - 1
        if diff < -0.75:
            stars.append(ICON.format('zmdi-star-outline'))
        elif diff < -0.25:
            stars.append(ICON.format('zmdi-star-half'))
        else:
            stars.append(ICON.format('zmdi-star'))
    return '<div class="star-rating no-select">{}</div>'.format(' '.join(stars))


@register.filter()
def distance(value):
    # return '{}km'.format(round(value, 1))
    return '{} km'.format(int(round(value)))


@register.assignment_tag(takes_context=True)
def get_url_name(context):
    try:
        return resolve(context.request.path_info).url_name
    except Resolver404:
        return None


@register.filter()
def as_unicode(value):
    return unicode(value)


@register.filter()
def get_cities(field):
    return City.objects.filter(id__in=field.value())


@register.filter()
def get_languages(field):
    return Language.objects.filter(id__in=field.value())


@register.filter()
def to_int_array(array):
    return map(int, array)


@register.filter()
def strip_tags(value):
    return strip_tags_original(value.replace('</h1>', '</h1> ').replace('</h2>', '</h2> ').replace('</h3>', '</h3> ').replace('</p><p>', ' '))


@register.filter()
def static_absolute(request, path):
    return request.build_absolute_uri(static(path)).strip()


@register.filter()
def absolute_url(request, path=None):
    return request.build_absolute_uri(path if path else request.path).strip()


@register.filter()
def bust(url):
    delimiter = '&' if ('?' in url) else '?'
    return url + delimiter + 'b=' + str(settings.STATIC_VERSION)


@register.filter()
def url_or_default(img):
    if img:
        return img.url
    else:
        return static('images/default.jpg')


@register.filter()
def div(a, b):
    if b == 0:
        return 0
    return float(a) / int(b)


@register.filter()
def sub(a, b):
    return int(a) - int(b)


@register.filter()
def mul(a, b):
    return int(a) * int(b)


@register.filter()
def flow_text(s):
    return mark_safe(s.replace('<p', '<p class="flow-text"'))


@register.filter()
def filter(img, filter):
    path, _, ext = img.file.name.partition('.')
    path_new = '.'.join((path, '_'.join(filter.split(',')), ext))

    m_path, _, m_ext = img.url.partition('.')
    m_path_new = '.'.join((m_path, '_'.join(filter.split(',')), m_ext))

    if not os.path.exists(path_new):
        img = Image.open(img.file.name)
        blurred = img.filter(ImageFilter.GaussianBlur(radius=3))
        blurred.save(path_new)

    return m_path_new


@register.filter()
def cut(html):
    if '<cut' in html:
        return html[:html.find('<cut')]
    return html


@register.filter()
def nl2sp(html):
    return html.replace('\r', '').replace('\n', ' ')


@register.filter()
def human_date(date):
    return u'{} тому'.format(format_timedelta(now() - date))


@register.simple_tag()
def get_setting(key):
    return getattr(settings, key, None)


@register.simple_tag()
def url_absolute(request, slug, *args, **kwargs):
    return request.build_absolute_uri(reverse(slug, args=args, kwargs=kwargs))


def do_graphize(match):
    src = HTMLParser().unescape(match.group(1))
    md5sum = hashlib.md5(src).hexdigest()
    filename = 'graph_{}.png'.format(md5sum)

    path = os.path.join(settings.MEDIA_ROOT, 'graphs', filename)
    m_path = settings.MEDIA_URL + 'graphs/' + filename

    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass

    if not os.path.exists(path):
        (graph,) = pydot.graph_from_dot_data(src)
        graph.create(format='png')
        graph.write_png(path)

    return '<figure><img src="http://dun.ai{}" class="responsive-nostretch" /></figure>'.format(m_path)


@register.filter()
def graphize(data):
    return re.sub('<pre class="graph">(.*)</pre>', do_graphize, data, flags=re.DOTALL)


@register.filter()
def fix(data):
    # data = re.sub(r'<img([^>]+[^/])>', '<img\\1 />', data, flags=re.DOTALL)
    # # data = re.sub(r'<figure><img([^>]+) /></figure>', '<img\\1 />', data, flags=re.DOTALL)
    # data = re.sub(r'<p([^>]+)>\s*(<figure>)?\s*<img([^>]+) />\s*(</figure>)?\s*</p>', '\\2<img\\3 />\\4', data, flags=re.DOTALL)
    # data = data.replace('<cut></cut>', '')
    # return data
    # doc = minidom.parseString('<html><body>' + data.encode('utf-8') + '</body></html>')

    doc = BS(data, 'html.parser')
    for img in doc.select('p > img'):
        print img
        p = img.parent
        p.replaceWith(img)

    for img in doc.select('img'):
        if isinstance(img.parent, BS):
            # No parent!
            parent = img.parent
            img_idx = parent.contents.index(img)
            figure = doc.new_tag('figure')
            figure.append(img)
            parent.insert(img_idx, figure)

        if img['src'].startswith('/'):
            img['src'] = 'http://dun.ai' + img['src']

    for figure in doc.select('figure'):
        if not isinstance(figure.parent, BS):
            if figure.parent.name == 'p':
                figure.parent.replaceWith(figure)

    for cut in doc.select('cut'):
        cut.extract()

    return doc.prettify()
