from django.conf.urls import url
import views


urlpatterns = [
    url('^$', views.index, name='index'),
    url('^item/(?P<item_id>\d+)$', views.item, name='item')
]
