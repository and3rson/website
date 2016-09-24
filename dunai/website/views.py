from django.http import HttpResponse
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from models import Category, Project, Tag, Contact
from django.core.urlresolvers import reverse


def make_error_handler(code, status):
    def error_handler(request):
        return render(request, 'dunai/error.jade', dict(
            code=code,
            status=status
        ))
    return error_handler


def make_file_server(file, content_type):
    def file_server(request):
        return HttpResponse(open(file, 'r'), content_type=content_type)
    return file_server


def index(request):
    return render(request, 'dunai/index.jade', dict(
        contacts=Contact.objects.order_by('order'),
        categories=Category.objects.order_by('order').prefetch_related(
            'projects', 'projects__tags'
        ),
        breadcrumbs=[
            dict(title='Andrew Dunai', url=reverse('website:index')),
        ],
        page='index'
    ))


def projects(request):
    return render(request, 'dunai/projects.jade', dict(
        contacts=Contact.objects.order_by('order'),
        categories=Category.objects.order_by('order').prefetch_related(
            'projects', 'projects__tags'
        ),
        breadcrumbs=[
            dict(title='Andrew Dunai', url=reverse('website:index')),
            dict(title='Projects', url=reverse('website:projects')),
        ],
        page='projects'
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
    return render(request, 'dunai/project.jade', dict(
        contacts=Contact.objects.order_by('order'),
        project=project,
        breadcrumbs=[
            dict(title='Andrew Dunai', url=reverse('website:index')),
            dict(title='Projects', url=reverse('website:projects')),
            dict(title=project.title, url=project.get_absolute_url())
        ],
        page='projects'
    ))
