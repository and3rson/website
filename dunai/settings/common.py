"""
Django settings for dunai project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import time

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DJANGO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DUNAI_SECRET_KEY', 'foo')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 'suit',
    # 'material',
    # 'material.admin',
    # 'jet.dashboard',
    # 'jet',
    'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'pyjade',
    'pyjade.ext.django',
    'static_precompiler',
    'django_markup',
    'ordered_model',
    'pagedown',
    'easy_thumbnails',
    'redactor',
    'memoize',

    'dunai.chat',
    'dunai.comics',
    'dunai.posts',
    'dunai.users',
    'dunai.website',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dunai.libs.middleware.ExceptionNotifier',
]

ROOT_URLCONF = 'dunai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': False,
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                # PyJade part:   ##############################
                ('pyjade.ext.django.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ))
            ],
            'builtins': ['pyjade.ext.django.templatetags'],
        },
    },
]

WSGI_APPLICATION = 'dunai.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'static_precompiler.finders.StaticPrecompilerFinder',
)

# STATIC_PRECOMPILER_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_PRECOMPILER_OUTPUT_DIR = 'gen'
STATIC_PRECOMPILER_MTIME_DELAY = 1

# Custom user model

AUTH_USER_MODEL = 'users.CustomUser'

# Static versioning
STATIC_VERSION = int(time.time())

# Media config
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Telegram config
TELEGRAM_TOKEN = os.getenv('DUNAI_TELEGRAM_TOKEN')
TELEGRAM_GROUP_ID = os.getenv('DUNAI_TELEGRAM_GROUP_ID')
TELEGRAM_CHANNEL_ID = '@shitworks'

# Django-jet

JET_INDEX_DASHBOARD = 'dunai.dashboard.CustomIndexDashboard'
# JET_DEFAULT_THEME = 'light-green'
JET_SIDE_MENU_COMPACT = True

JET_SIDE_MENU_CUSTOM_APPS = [
    (
        'users',
        [
            'CustomUser',
        ]
    ),
    (
        'auth',
        [
            'Group',
        ]
    ),
    (
        'website',
        [
            'Category',
            'Project',
            'Tag',
            'Link',
            'Provider',
            'Screenshot',
            'Contact',
        ]
    ),
    (
        'comics',
        [
            'Comic',
        ]
    ),
    (
        'posts',
        [
            'Post',
            'Category',
        ]
    ),
]

REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = 'uploads/'

# django-admin-bootstrap
BOOTSTRAP_ADMIN_SIDEBAR_MENU = True

# FB config
FB_APP_ID = 1439213499662726
FB_PAGE_ID = 542844375818862

# Cache config
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'dunai',
    }
}

# Fonts
FONTS_DIR = os.path.join(BASE_DIR, 'website/static/fonts')
