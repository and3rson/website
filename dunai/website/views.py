from django.shortcuts import render
from models import Project


def index(request):
    projects = Project.objects.all()
    return render(request, 'dunai/index.jade', dict(
        projects=projects
    ))


def project(request, item_id):
    return render(request, 'dunai/project.jade')
