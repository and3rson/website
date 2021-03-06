from django.shortcuts import render, get_object_or_404
from dunai.comics.models import Comic
from django.core.urlresolvers import reverse
from dunai.website.models import Contact


def view_comics(request):
    comics = Comic.objects.order_by('-added_on')
    return render(request, 'dunai/comics.jade', dict(
        contacts=Contact.objects.order_by('order'),
        comics=comics,
        breadcrumbs=[
            dict(title='Andrew Dunai', url=reverse('website:index')),
            dict(title='Comics', url=reverse('comics:list')),
        ],
        page='comics'
    ))


def view_comic(request, comic_slug):
    comic = get_object_or_404(Comic, slug=comic_slug)

    return render(request, 'dunai/comic.jade', dict(
        contacts=Contact.objects.order_by('order'),
        comic=comic,
        breadcrumbs=[
            dict(title='Andrew Dunai', url=reverse('website:index')),
            dict(title='Comics', url=reverse('comics:list')),
            dict(title=comic.title, url=comic.get_absolute_url())
        ],
        page='comics'
    ))
