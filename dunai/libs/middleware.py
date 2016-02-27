import traceback
from django.core.urlresolvers import resolve
from django.http import HttpResponsePermanentRedirect, HttpResponse, Http404
# from django.http.response import REASON_PHRASES
from dunai.libs.notifier import Notifier
from django.conf import settings
from re import sub


class ExceptionNotifier(object):
    def process_exception(self, request, exception):
        if not settings.DEBUG:
            if isinstance(exception, Http404):
                return
            exc = u'Error at {}:\n\n'.format(request.path)
            error_lines = traceback.format_exc().split('\n')
            # error_lines = error_lines[:3] + error_lines[3:5] * 100 + error_lines[5:]

            frames_skipped = 0
            while len('\n'.join(error_lines)) > 4000 or len(error_lines) > 22:
                error_lines = error_lines[:3] + error_lines[5:]
                frames_skipped += 1

            if frames_skipped > 0:
                error_lines = error_lines[:3] + ['  ' + '=' * 11, '  ({} frames skipped)'.format(frames_skipped), '  ' + '=' * 11] + error_lines[3:]

            exc += '```' + '\n'.join(error_lines) + '```'
            Notifier.notify(exc, parse_mode='Markdown', tags='web error')


# class DomainCheckMiddleware(object):
#     def process_request(self, request):
#         host = request.get_host()
#
#         if not settings.DEBUG and host != 'testserver':
#             host = sub('^www\.', '', host)
#             host = sub(':[\d]{2,5}$', '', host)
#
#             if host not in ('roam.in.ua', 'onjaunt.com', 'roaming.org'):
#                 return HttpResponsePermanentRedirect('http://onjaunt.com')
#
#
# class GoogleTrackerMiddleware(object):
#     def process_response(self, request, response):
#         content_type = response.get('Content-Type')
#
#         bot = None
#         tag = None
#
#         if content_type and content_type.startswith('text/html'):
#             agent = request.META.get('HTTP_USER_AGENT')
#             if agent:
#                 if 'googlebot' in agent.lower():
#                     bot = 'GOOGLE BOT'
#                     tag = 'google'
#                 elif 'yandexbot' in agent.lower():
#                     bot = 'YANDEX BOT'
#                     tag = 'yandex'
#                 elif 'bingbot' in agent.lower():
#                     bot = 'BING BOT'
#                     tag = 'bing'
#                 elif 'msnbot' in agent.lower():
#                     bot = 'MSN BOT'
#                     tag = 'msn'
#                 elif 'yahoo! slurp' in agent.lower():
#                     bot = 'YAHOO! SLURP BOT'
#                     tag = 'slurp'
#
#                 if bot and tag:
#                     Notifier.notify(
#                         'Indexing "{}", status: {}'.format(request.path, response.status_code),
#                         tags='bots {}'.format(tag)
#                     )
#
#         if not (bot or tag):
#             if response.status_code in (400, 403, 404):
#                 Notifier.notify('Someone got {} on "{}"'.format(response.status_code, request.path), tags='web error')
#
#         return response
#
#
# TEAPOT_RESPONSE = '''<html>
#     <head>
#         <title>418 {response}</title>
#     </head>
#     <body>
#         <h1>418 {response}</h1>
#     </body>
# </html>'''
#
#
# class HTCPCPMiddleware(object):
#     def process_request(self, request):
#         if request.method.upper() in ('BREW', 'WHEN'):
#             return HttpResponse(TEAPOT_RESPONSE.format(response=REASON_PHRASES.get(418)) + '\n', status=418)
