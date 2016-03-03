from django.shortcuts import render, get_object_or_404
from dunai.comics.models import Comic


def view_comics(request):
    comics = Comic.objects.order_by('-added_on')
    return render(request, 'dunai/comics.jade', dict(
        comics=comics
    ))


def view_comic(request, comic_slug):
    return render(request, 'dunai/_comic.jade' if 'nested' in request.GET else 'dunai/comic.jade', dict(
        comic=get_object_or_404(Comic, slug=comic_slug)
    ))
