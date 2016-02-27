#!/usr/bin/env /var/apps/dunai/.env/bin/python2.7

#  // @-k gevent
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dunai.settings.prod")

from dunai import wsgi

app = wsgi.application
