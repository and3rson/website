from django.conf.urls import url
import views

urlpatterns = [
    url('^$', views.view, name='view'),
    url('^set_name$', views.set_name, name='set-name'),
    url('^poll$', views.poll, name='poll'),
    url('^send$', views.send, name='send')
]
