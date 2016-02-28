from .common import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dunai',
        'HOST': 'localhost',
        'PORT': 5432,
        'USER': 'anderson',
        'PASS': '',
    }
}
