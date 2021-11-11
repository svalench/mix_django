"""
Django settings for mix_django project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4a%m+5z9x_z!4z6e3vpbgd#&nrx=o8v&r1xdc=(sn%+x^#cjxj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['api.mixenerdgy.by', 'localhost', '127.0.0.1', 'www.api.mixenerdgy.by']


# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.gis',
    'admin_reorder',
    'rest_framework.authtoken',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'user',
    'catalog',
    'product',
    'dynamic_raw_id',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'mix_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'mix_django.wsgi.application'
CORS_ORIGIN_ALLOW_ALL = True

AUTH_USER_MODEL = 'user.User'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
print(os.environ)
if os.environ.get('prod')!='':
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('name_django_db'),
        'USER': os.environ.get('user_django_db'),
        'PASSWORD': os.environ.get('password_django_db'),
        'HOST': 'localhost',
        'PORT': 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'ru'
LOCALES = ['ru', 'en', 'ua', 'by']
TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.BasePermission',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10


}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/').replace('\\', '/')
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#======GEOLOC==============
# SPATIALITE_LIBRARY_PATH = 'C:\\Users\\алексадр\\PycharmProjects\\beautymasters\\venv\\Scripts\\mod_spatialite'
SPATIALITE_LIBRARY_PATH = 'mod_spatialite'
GEOIP_PATH = BASE_DIR / 'mix_django/geoip/GeoLite2-City_20210810'
# if os.name == 'nt':
#     VIRTUAL_ENV_BASE = os.environ['VIRTUAL_ENV']
#     os.environ['PATH'] = os.path.join(VIRTUAL_ENV_BASE, r'.\Lib\site-packages\osgeo') + ';' + os.environ['PATH']
#     os.environ['PROJ_LIB'] = os.path.join(VIRTUAL_ENV_BASE, r'.\Lib\site-packages\osgeo\data\proj') + ';' + os.environ['PATH']


ADMIN_REORDER = (
    {'app': 'product', 'label': 'Продукты',
     'models': ('product.CardProduct', 'product.Product', 'product.ProductsImages')
    },
    {'app': 'product', 'label': 'Фильтра',
     'models': ('product.Filters', 'product.FiltersValue', 'product.Units')
    },
    {'app': 'product', 'label': 'Характеристики',
     'models': ('product.Characteristics', 'product.CharacteristicValue', 'product.Units')
    },
    {'app': 'catalog', 'label': 'Категории',
     'models': ('catalog.FirstCategory', 'catalog.SecondCategory')
    },
    {'app': 'catalog', 'label': 'Документы',
     'models': ('catalog.DocumentsCard',)
    },
    {'app': 'user', 'label': 'Пользователи',
     'models': ('user.User', 'user.Carts')
    },
)

GRAPPELLI_ADMIN_TITLE = 'MixEnergy'


#==========================EMAIL SETTINGS==========================================================/

# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
EMAIL_HOST = 'ssl://smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'mixenerdgy.by@yandex.by'
EMAIL_HOST_PASSWORD = '8940113Wert'

DOMAIN = 'api.mixenerdgy.by'
MANAGER_EMAIL = 'mixenerdgy@mail.ru'
#==================================================================================================
#==================================================================================================