from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from models import Category, Project, Tag


def index(request):
    categories = Category.objects.order_by('order').prefetch_related('projects', 'projects__tags')
    return render(request, 'dunai/index.jade', dict(
        categories=categories
    ))


def view_project(request, item_id):
    project = get_object_or_404(
        Project.objects.prefetch_related(
            Prefetch('tags', Tag.objects.order_by('-importance')),
            'screenshots',
            'links',
            'links__provider'
        ),
        pk=item_id
    )
    return render(request, 'dunai/_project.jade' if 'nested' in request.GET else 'dunai/project.jade', dict(
        project=project
    ))
