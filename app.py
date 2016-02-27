#!/usr/bin/env python2.7
#@-k gevent
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roaming.settings.prod")

from dunai import wsgi

app = wsgi.application
