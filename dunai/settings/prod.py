from .common import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dunai',
        'HOST': 'localhost',
        'PORT': 5433,
        'USER': 'anderson',
        'PASS': '',
    }
}
