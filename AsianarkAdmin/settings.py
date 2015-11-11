"""
Django settings for AsianarkAdmin project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c+p*di2k@3w89sg1c^)s^o*blc*w#o0407oq84ihs$l_m1oyrt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  #set '*' when DEBUG = Falase

ADMIN = (('Thomas', 'thomas_lee@outlook.de'), ) # send email to the address when DEBUG = False and error raise

# Application definition

INSTALLED_APPS = (
    'AsianarkAdmin.suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'AsianarkAdmin.admin_ip_whitelist',
    'AsianarkAdmin.userinfo',
    'AsianarkAdmin.baccarat_Controll',
    'AsianarkAdmin.serverinfo',
    #'debug_toolbar',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    #'AsianarkAdmin.admin_ip_whitelist.middleware.AdminAcceessIPWhiteListMiddleware'
)

ADMIN_ACCEES_WHITELIST_ENABLED = False

ADMIN_ACCEES_WHITELIST_MESSAGE = 'Your ip address is not allowed!'

ROOT_URLCONF = 'AsianarkAdmin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                #'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'AsianarkAdmin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bjl',                      # Or path to database file if using sqlite3.
        'USER': 'web',                      # Not used with sqlite3.
        'PASSWORD': 'web.ak',                  # Not used with sqlite3.
        'HOST': '202.77.29.210',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = ''

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

#AUTH_USER_MODULE = 'AsianarkAdmin.TControllers'

BOWER_INSTALLED_APPS = (
    'jquery',
    'underscore',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        "HOSTNAME":'bjl',
    }
}

TIMEOUT = None   #cache time out!

#Game Server
GAME_SERVER = {
    'dafault':{
        'URL':'127.0.0.1',
        'PORT':'2012',
        'NAME':'bjl_Game_Ser'
    }
}

#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True

