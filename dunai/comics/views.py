from django.shortcuts import render
from dunai.comics.models import Comic


def view_comics(request):
    comics = Comic.objects.order_by('-added_on')
    return render(request, 'dunai/comics.jade', dict(
        comics=comics
    ))
