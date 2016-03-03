from django.conf.urls import url
from dunai.comics import views

urlpatterns = [
    url('^$', views.view_comics, name='list'),
    url('^/(?P<comic_slug>[a-zA-Z0-9_-]+)$', views.view_comic, name='view')
]
