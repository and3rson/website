from django.conf.urls import url
import views


urlpatterns = [
    url('^$', views.index, name='index'),
    url('^projects/(?P<item_id>\d+)$', views.view_project, name='project')
]
