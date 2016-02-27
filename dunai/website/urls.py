from django.conf.urls import url
import views


urlpatterns = [
    url('^$', views.index, name='index'),
    url('^project/(?P<item_id>\d+)$', views.project, name='item')
]
