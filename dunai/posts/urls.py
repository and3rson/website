from django.conf.urls import url
from dunai.posts import views

urlpatterns = [
    url('^$', views.view_posts, name='list'),
    url('^(?P<post_slug>[a-zA-Z0-9_-]+)$', views.view_post, name='view'),
    url('^(?P<post_slug>[a-zA-Z0-9_-]+)/cover.jpg$', views.view_post_cover, name='view-cover')
]
