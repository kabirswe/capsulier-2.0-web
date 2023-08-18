""" Settings """

import os
from mahdil.variables.admin_reorder import *
from mahdil.variables.all_auth import *
from mahdil.variables.ckeditor import *
from mahdil.variables.cropping import *
from mahdil.variables.env_variables import *
from mahdil.variables.language import *
from mahdil.variables.select2 import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Hosts
ALLOWED_HOSTS = [
    'preprod.conservatoireducafe.fr',
    'preprod.lecapsulier.fr',
    'preprod2.lecapsulier.fr',
    'conservatoireducafe.fr',
    'www.conservatoireducafe.fr',
    'lecapsulier.fr',
    'www.lecapsulier.fr',
    'localhost',
]

if DEBUG:
    DEFAULT_FROM_EMAIL = 'Le Conservatoire du Cafe / Le Capsulier<contact@conservatoireducafe.fr>'
    EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
    ANYMAIL = {
        'MAILGUN_API_KEY': 'key-3b8ab6c1476d4ce92754469dc75dbffc',
        'MAILGUN_SENDER_DOMAIN': 'mg.lecapsulier.fr',
    }
else:
    DEFAULT_FROM_EMAIL = 'Le Conservatoire du Cafe / Le Capsulier<contact@conservatoireducafe.fr>'
    EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
    ANYMAIL = {
        'MAILGUN_API_KEY': 'key-3b8ab6c1476d4ce92754469dc75dbffc',
        'MAILGUN_SENDER_DOMAIN': 'mg.lecapsulier.fr',
    }

# Application definition
INSTALLED_APPS = [

    # Third Party Apps
    'flat_responsive',
    'modeltranslation',

    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django Additional Apps
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.redirects',

    # Third Party Apps
    'adminsortable2',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'anymail',
    'ckeditor',
    'ckeditor_uploader',
    'colorful',
    'crispy_forms',
    'django_cleanup',
    'django_countries',
    'django_filters',
    'django_unused_media',
    'easy_select2',
    'easy_thumbnails',
    'geoposition',
    'image_cropping',
    'import_export',
    'rest_framework',
    'widget_tweaks',

    # Mahdil Apps
    'blog',
    'contact',
    'eshop',
    'main',
    'mycaps',
    'page',
    'product',
    # 'promotions',
    'userprofile',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Sites
    'django.contrib.sites.middleware.CurrentSiteMiddleware',

    # Modeltransaltion
    'django.middleware.locale.LocaleMiddleware',

    # Admin Reorder
    # 'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'mahdil.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Mahdil
                'mahdil.context_processors.mahdil_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'mahdil.wsgi.application'


# Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# Internationalization
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
if not MAHDIL_LIVE or MAHDIL_STATIC_LOCAL:
    STATIC_URL = '/static/'
else:
    STATIC_URL = 'http://static.lecapsulier.fr/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn')


# Media files (uploads)
if not MAHDIL_LIVE or MAHDIL_MEDIA_LOCAL:
    MEDIA_URL = '/media/'
else:
    MEDIA_URL = 'http://media.lecapsulier.fr/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media_cdn')

FILE_UPLOAD_PERMISSIONS = 0644

# Crispy FORM TAGs SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Phonenumber Fields
PHONENUMBER_DB_FORMAT = 'INTERNATIONAL'
PHONENUMBER_DEFAULT_REGION = 'FR'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
    }
}
# if MAHDIL_LIVE:
#     # Constants
#     GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyDdfNK2L9RMM7YFCo8g9YaZHcm-qqPscfI'

#     # Database
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': MAHDIL_SQL,
#             'USER': MAHDIL_SQL,
#             'PASSWORD': PASSWORD_SQL_MAHDIL_LIVE,
#             'HOST': MAHDIL_HOST,
#             'PORT': '3306',
#             'OPTIONS': {
#                 'init_command': 'SET default_storage_engine=INNODB; SET sql_mode=STRICT_TRANS_TABLES',
#             },
#         }
#     }
# else:
#     # Constants
#     GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyDdfNK2L9RMM7YFCo8g9YaZHcm-qqPscfI'

#     MAILCHIMP_API_KEY = '8e1fa74476cf67adce093ac2c34ed9b8-us14'
#     MAILCHIMP_LIST_ID = '452d50c560'

#     # Database
#     if MAHDIL_SQLITE:
#         DATABASES = {
#             'default': {
#                 'ENGINE': 'django.db.backends.sqlite3',
#                 'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
#             }
#         }
#     else:
#         DATABASES = {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'NAME': MAHDIL_SQL,
#                 'USER': 'root',
#                 'PASSWORD': '',
#                 'HOST': '127.0.0.1',
#                 'PORT': '3306',
#                 'OPTIONS': {
#                     'init_command': 'SET default_storage_engine=INNODB; SET sql_mode=STRICT_TRANS_TABLES',
#                 },
#             }
#         }
