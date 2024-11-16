import dj_database_url
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hxyz71c)#===vrx&7nzz0=h!a1@genp)p@v($l%t=a+#649mj7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

SITE_WHATSAPP_NO = "+2348162467444"

SITE_URL = "http://127.0.0.1:8000"



JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "DonLiora Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "DonLiora",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "DonLiora",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "img/logo/logo-name.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "img/logo/icon-jazz.png",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": "img/logo/logo-name-dark.png",

    # CSS classes that are applied to the logo above
    "site_logo_classes": ["logo"],

    "custom_css": "css/style.css",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "img/logo/icon-jazz.png",

    # Welcome text on the login screen
    "welcome_sign": "Welcome Admin!",

    # Copyright on the footer
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
            os.path.join(BASE_DIR,"core/templates"),
            os.path.join(BASE_DIR,"shop/templates"),
            os.path.join(BASE_DIR,"shop/templates/components"),
            os.path.join(BASE_DIR,"fashion/templates/components"),
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


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEBUG :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            "OPTIONS": {
                "timeout": 30,
            }
        },
        "OPTIONS": {
        # ...
        "timeout": 30,
        # ...
    }
    }

else :
    # Replace the SQLite DATABASES configuration with PostgreSQL:

    DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost:5432/mydatabase')
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,"media")

STATICFILES_DIRS = [
os.path.join(BASE_DIR,"static")
]


LOGIN_REDIRECT_URL = 'login-redirect'

LOGOUT_REDIRECT_URL = 'index'
STATIC_URL = '/static/'

#EMAIL FOR ZOHO
EMAIL_HOST  = "smtp.zoho.com"
EMAIL_PORT = "587"
#for other emails 
EMAIL_HOST_USER = "support@donliora.com"
DEFAULT_FROM_EMAIL  = "support@donliora.com"
EMAIL_HOST_PASSWORD = '#Thop!$9!!0f'
EMAIL_HOST_USER_LOGISTICS = "logistics@donliora.com"
EMAIL_HOST_USER_SUPPORT = "support@donliora.com"

EMAIL_USE_TLS = "True"

SITE_NAME = "StylezbyDee"
SITE_ADDRESS = "https://www.stylezbydee.com/"

STATIC_ROOT = os.path.join(BASE_DIR,"asset")

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
 

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
