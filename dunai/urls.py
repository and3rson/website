# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from dunai.website.views import make_error_handler, make_file_server
import os
# from jet.dashboard.dashboard_modules import google_analytics_views


urlpatterns = [
    # url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^admin/', admin.site.urls),
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^', include('dunai.website.urls', namespace='website')),
    url(r'^comics/', include('dunai.comics.urls', namespace='comics')),
    url(r'^chat/', include('dunai.chat.urls', namespace='chat')),
    url(r'^posts/', include('dunai.posts.urls', namespace='posts')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^test-error$', lambda request: 1 / 0, name='test-error'),
    url(
        r'^favicon.ico',
        make_file_server(
            os.path.join(settings.BASE_DIR, 'website/static/images/favicon.png'),
            'image/png'),
        name='favicon'
    )
]

handler404 = make_error_handler(404, u'НЕ ЗНАЙДЕНО')
handler500 = make_error_handler(500, u'ПОМИЛКА СЕРВЕРА')

urlpatterns += [
    url(r'^404$', handler404, name='error-404'),
    url(r'^500$', handler500, name='error-500'),
]
