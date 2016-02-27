from django.shortcuts import render


def index(request):
    return render(request, 'dunai/index.jade')


def item(request, item_id):
    return render(request, 'dunai/item.jade')
