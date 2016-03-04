from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from dunai import resources

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('dunai.website.urls', namespace='website')),
    url(r'^comics/', include('dunai.comics.urls', namespace='comics')),
    url(r'^chat/', include('dunai.chat.urls', namespace='chat')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^test-error$', lambda request: 1/0, name='test-error'),
    url(r'^favicon\.ico$', resources.serve_static('images/favicon.png', 'image/png', render=False), name='favicon')
]
