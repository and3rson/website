from django.conf.urls import url
from dunai.comics import views

urlpatterns = [
    url('^$', views.view_comics, name='comics')
]
