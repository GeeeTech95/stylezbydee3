import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load sensitive settings from .env
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# Site information
SITE_NAME  = config('SITE_NAME')
SITE_ADDRESS = config('SITE_ADDRESS')
SITE_WHATSAPP_NO = config('SITE_WHATSAPP_NO')
SITE_URL = config('SITE_URL')

# Jazzmin settings
JAZZMIN_SETTINGS = {
    "site_title": "DonLiora Admin",
    "site_header": "DonLiora",
    "site_brand": "DonLiora",
    "site_logo": "img/logo/logo-name.png",
    "login_logo": "img/logo/icon-jazz.png",
    "login_logo_dark": "img/logo/logo-name-dark.png",
    "site_logo_classes": ["logo"],
    "custom_css": "css/style.css",
    "site_icon": "img/logo/icon-jazz.png",
    "welcome_sign": "Welcome Admin!",
    "copyright": "DonLiora",
}

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'shop.apps.ShopConfig',
    'fashion.apps.FashionConfig',
    'order.apps.OrderConfig',
    'cart.apps.CartConfig',
    'treebeard',
    'whitenoise.runserver_nostatic',
    'crispy_forms',
    'django_filters',
    'phonenumber_field',
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'donliora.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "core/templates"),
            os.path.join(BASE_DIR, "shop/templates"),
            os.path.join(BASE_DIR, "shop/templates/components"),
            os.path.join(BASE_DIR, "fashion/templates/components"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context.core',
            ],
        },
    },
]

WSGI_APPLICATION = 'donliora.wsgi.application'

# Database configuration
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# Password validation
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

AUTH_USER_MODEL = "users.User"

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "asset")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Login and logout redirects
LOGIN_REDIRECT_URL = 'login-redirect'
LOGOUT_REDIRECT_URL = 'index'

# Email configuration
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER_LOGISTICS = config('EMAIL_HOST_USER_LOGISTICS')
EMAIL_HOST_USER_SUPPORT = config('EMAIL_HOST_USER_SUPPORT')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

