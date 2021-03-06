from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template.loader import get_template
from dunai.posts.models import Post
from dunai.website.models import Contact
from .helpers import get_share_count
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
from resizeimage import resizeimage
from feedgen.feed import FeedGenerator
from dunai.website.templatetags import common as tags


def view_posts(request):
    posts = Post.objects.order_by('-date_added').prefetch_related('categories')
    return render(request, 'dunai/posts.jade', dict(
        contacts=Contact.objects.order_by('order'),
        posts=posts,
        breadcrumbs=[
            dict(title='Andrew Dunai', url=reverse('website:index')),
            dict(title='Posts', url=reverse('posts:list')),
        ],
        page='posts'
    ))


def view_post(request, post_slug):
    post = get_object_or_404(Post.objects.prefetch_related('categories'), slug=post_slug)

    if 'HTTP_X_FORWARDED_FOR' in request.META:
        post.add_view(request.META['HTTP_X_FORWARDED_FOR'].partition(',')[0])
        post.save()

    likes = get_share_count(request.build_absolute_uri(post_slug))

    # next_post = Post.objects.filter(date_added__gt=post.date_added).order_by('date_added').prefetch_related('categories').first()
    # prev_post = Post.objects.filter(date_added__lt=post.date_added).order_by('-date_added').prefetch_related('categories').first()
    other_posts = Post.objects.exclude(pk=post.pk).order_by('?')[:3]

    return render(request, 'dunai/post.jade', dict(
        contacts=Contact.objects.order_by('order'),
        post=post,
        likes=likes,
        # prev_post=prev_post,
        # next_post=next_post,
        other_posts=other_posts,
        breadcrumbs=[
            dict(title='Andrew Dunai', url=reverse('website:index')),
            dict(title='Posts', url=reverse('posts:list')),
            dict(title=post.title, url=post.get_absolute_url()),
        ],
        page='posts'
    ))


def view_post_cover(request, post_slug):
    font_size = 48
    size = (640, 480)

    # print settings.BASE_DIR
    post = get_object_or_404(Post.objects.prefetch_related('categories'), slug=post_slug)
    text = post.title

    img = Image.open(post.cover.file.name)
    # img.thumbnail(size, Image.ANTIALIAS)
    img = resizeimage.resize_cover(img, size)
    draw = ImageDraw.Draw(img, 'RGBA')

    # Shade
    draw.rectangle((0, 0,) + img.size, fill=(0, 0, 0, 160))

    # Font
    font = ImageFont.truetype(os.path.join(settings.FONTS_DIR, 'Roboto-Light.ttf'), size=font_size)

    avg_width = draw.textsize(text, font)[0] / len(text) + size[0] / 150
    chars_per_line = img.size[0] / avg_width
    text = '\n'.join(textwrap.wrap(text, width=chars_per_line))

    text_bbox = draw.multiline_textsize(text, font)

    # Draw text
    x, y = ((size[0] - text_bbox[0]) / 2, (size[1] - text_bbox[1]) / 2)
    draw.multiline_text((x + 1, y + 3), text, fill=(0, 0, 0, 128), font=font, align='center')
    draw.multiline_text((x, y), text, fill='#FFF', font=font, align='center')

    response = HttpResponse(content_type='image/jpeg')
    img.save(response, 'JPEG')
    return response


def feed(request):
    posts = Post.objects.prefetch_related('categories').order_by('-date_added')[:20]

    gen = FeedGenerator()
    gen.title('Andrew Dunai')
    gen.author(dict(name='Andrew Dunai', email='andrew@dun.ai'))
    gen.link(href=request.build_absolute_uri('/'))
    gen.description('Latest posts & comics by Andrew Dunai.')

    template = get_template('dunai/instant_post.jade')

    for post in posts:
        entry = gen.add_entry()
        entry.id('{}-{}'.format(post.id, post.slug))

        entry.title(post.title)
        entry.link(href=request.build_absolute_uri(post.get_absolute_url()))
        entry.description(tags.strip_tags(tags.cut(post.content.replace('\n', ' ').replace('\r', ''))))
        entry.pubdate(post.date_added)
        entry.author(dict(name='Andrew Dunai', email='andrew@dun.ai'))
        entry.content(template.render(dict(request=request, post=post)), type='CDATA')
        # entry.content(tags.graphize(post.content.replace('<cut></cut>', '')), type='CDATA')

    return HttpResponse(gen.rss_str(pretty=True))
