"""
    Created by Chicherov Oleg 2016
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y)9+o=_dry%eozza7yrdwhcsh$%kn2xxex_q+b#w462hk*9!6x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/auth/login/'
# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
    'testsConstructor',
    'users',
    'tests',
    'constructor',
    'analytics',
    'loginsys'
]


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


REST_FRAMEWORK = {
    'FORM_METHOD_OVERRIDE': None,
    'FORM_CONTENT_OVERRIDE': None,
    'FORM_CONTENTTYPE_OVERRIDE': None
}

ROOT_URLCONF = 'testsConstructor.urls'
#Кроссерверные запросы
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'loginsys/templates'),
            os.path.join(BASE_DIR, 'users/templates'),
            os.path.join(BASE_DIR, 'constructor/templates'),
            os.path.join(BASE_DIR, 'tests/templates'),
            os.path.join(BASE_DIR, 'analytics/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'testsConstructor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'main.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'analytics/static'),
    os.path.join(BASE_DIR, 'tests/static')
]

MEDIA_ROOT = BASE_DIR + '/media/'
MEDIA_URL = '/media/'

SUIT_CONFIG = {
    'ADMIN_NAME': 'Конструктор Тестов',
    'MENU_ICONS': {
        'constructor': 'icon-cog',
        'tests': 'icon-tasks',
        'users': 'icon-user',
        'analytics': 'icon-leaf'
    },
    'MENU_EXCLUDE': ('auth', )
}