"""
Django settings for unlimited Studio project.

Generated by 'django-myadmin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import pymysql
import django_heroku
import dj_database_url
pymysql.install_as_MySQLdb()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v0h!u1#176+u4sbdfolkqe33gcn9ht&t66*@-*jma#-_^p#g9j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'widget_tweaks',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'setting',
    'myadmin',
    'rest_framework',
    'rest_framework_datatables',
    'rest_framework.authtoken',
    'fcm_django',
    'django_filters',

]

LOGIN_REDIRECT_URL='myadmin/dashboard/'
LOGIN_URL='myadmin/login/'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    "EXCEPTION_HANDLER": "unlimitedstudio.apiutils.custom_exception_handler",
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 50,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]


ROOT_URLCONF = 'unlimitedstudio.urls'
# MESSAGE_STORAGE='django.contrib.messages.storage.session.SessionStorage'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'unlimitedstudio.context_processors.site_constants',
            ],
        },
    },
]

WSGI_APPLICATION = 'unlimitedstudio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'unlimitedstudio',
#         'USER': 'root',
#         'PASSWORD': 'root',
#         'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
email_url="127.0.0.1:8000"
base_url="http://127.0.0.1:8000"
STRIPE_SECRET_KEY=""
STRIPE_CLIENT_ID=""
fcmkey=""


# LOGIN_REDIRECT_URL = 'dashboard'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

"""

SENDGRID_API_KEY = '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'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # always use this
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY # sendgrid.com/settings/api_keys
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = "yodhagiri@gmail.com"
SENDGRID_SANDBOX_MODE_IN_DEBUG=False
EMAIL_USE_TLS = True

"""
EMAIL_HOST = 'mail.ninehertzindia.com'
EMAIL_HOST_USER = 'test@ninehertzindia.com'
EMAIL_HOST_PASSWORD = 'Test@12345'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = "rakesh@yopmail.com"
EMAIL_USE_TLS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOGIN_URL = 'login'
AUTH_USER_MODEL = 'user.User'



'''
Site Constants
'''
MEDIA_PATH = 'media'
APP_NAME = 'UnlimitedStudio'
APP_DOMAIN = 'localhost:8000'
APP_PROTOCOL = 'http'
BASE_URL = APP_PROTOCOL+"://"+APP_DOMAIN
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
ADD_SUCCESS_MESSAGE = 'Record added successfully'
UPDATE_SUCCESS_MESSAGE = 'Record updated successfully'
PERMISSION_DENIED_MESSAGE = 'Permission Denied'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

django_heroku.settings(locals())
