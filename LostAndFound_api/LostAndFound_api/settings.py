"""
Django settings for LostAndFound_api project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!h&ifv=l0e-gw%1(+_@wp!23^9j@yw8bd@4eu1ysw$)n(k*@bb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'goods.apps.GoodsConfig',
    'user',
    'index',
    'xadmin',
    'crispy_forms',
    'rest_framework',
    'reversion',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LostAndFound_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'LostAndFound_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'laf',
        'PORT': 3306,
        'HOST': '127.0.0.1',
        'PASSWORD': '123456',
        'USER': 'root'
    }
}

# redis????????????
CACHES = {
    # ????????????
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # ?????????redis??????
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # ??????
    "sms_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        # ?????????redis??????
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
# DRF???????????????
REST_FRAMEWORK = {
    # DRF????????????????????????????????????
    'EXCEPTION_HANDLER': 'utils.MyException.exception_handler',
    # ??????????????????
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'user.myauth.MyAuth',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# ??????????????????
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# ????????????
LOGGING = {
    # ????????????
    'version': 1,
    # ?????????????????????????????????
    'disable_existing_loggers': False,
    # ?????????????????????
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    # ??????????????????
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # ?????????????????????
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        # ???????????????????????????
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs/flower_api.log"),
            # ???????????????  ??????????????????100M
            'maxBytes': 100 * 1024 * 1024,
            # ???????????????????????????
            'backupCount': 10,
            # ?????????????????????
            'formatter': 'verbose'
        },
    },
    # ????????????
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,  # ???????????????????????????????????????????????????????????????
        },
    }
}

# ??????????????????
CORS_ORIGIN_ALLOW_ALL = True
AUTH_USER_MODEL = "user.UserInfo"
AUTHENTICATION_BACKENDS = [
    "user.utils.UserAuthBackend",
]

# JWT??????
JWT_AUTH = {
    # token???????????????
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=60 * 60 * 24),
    # ?????????jwt?????????
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'user.utils.jwt_response_payload_handler',
}
