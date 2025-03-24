import dj_database_url
import os
from pathlib import Path
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Security settings for production
"""SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
"""
# Strong secret key
SECRET_KEY = 'y0uR$ecR3tK3y-!@#R4nD0mly-Gen3Rat3d-FoR$3cUrity&STaBil1ty'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'
#DEBUG  = False

ALLOWED_HOSTS = ['*']

SITE_WHATSAPP_NO = "+2348162467444"
SITE_URL = "http://127.0.0.1:8000"



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}


UNFOLD = {
    "SITE_TITLE": "Stylezbydee Admin",
    "SITE_HEADER": "HGello",
    "SITE_URL": "/",
    # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    "SITE_ICON": {
        "light": lambda request: static("icon-light.svg"),  # light mode
        "dark": lambda request: static("icon-dark.svg"),  # dark mode
    },
    # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    "SITE_LOGO": {
        "light": lambda request: static("logo-light.svg"),  # light mode
        "dark": lambda request: static("logo-dark.svg"),  # dark mode
    },
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon.svg"),
        },
    ],
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    # "ENVIRONMENT": "fashion.environment_callback",
    # "DASHBOARD_CALLBACK": "fashion.dashboard_callback",
    "THEME": "light",  # Force theme: "dark" or "light". Will disable theme switcher
    "LOGIN": {
        "image": lambda request: static("img/studio/DSC_0944.jpg"),

    },

}


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "StylezByDee Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "StylezByDee",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "StylezByDee",

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
    "copyright": "StylezByDee",
}


# Application definition
INSTALLED_APPS = [
    #'jazzmin',
    "unfold",  # before django.contrib.admin
    # "unfold.contrib.filters",  # optional, if special filters are needed
    # "unfold.contrib.forms",  # optional, if special form elements are needed
    # "unfold.contrib.inlines",  # optional, if special inlines are needed
    # "unfold.contrib.import_export",  # optional, if django-import-export package is used
    # "unfold.contrib.guardian",  # optional, if django-guardian package is used
    # optional, if django-simple-history package is used
    # "unfold.contrib.simple_history",
    "django.contrib.admin",  # required
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
    'myadmin.apps.MyadminConfig',

    'treebeard',

    'whitenoise.runserver_nostatic',
    'crispy_forms',
    'django_filters',
    'phonenumber_field',

    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'storages',
    'cloudinary',
    'cloudinary_storage',
]

"""if DEBUG :
    INSTALLED_APPS += [ "django_browser_reload"]"""



CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dqlbvzdhx',
    'API_KEY': '491664366214778',
    'API_SECRET': 'EroTArEsCH4bJhkApAQl4_bijIA',
    
}

if DEBUG :
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

else:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


CRISPY_TEMPLATE_PACK = 'bootstrap4'  # or 'bootstrap5'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # whitenoise
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

"""if DEBUG:
    MIDDLEWARE += ['django_browser_reload.middleware.BrowserReloadMiddleware']"""

ROOT_URLCONF = 'stylezbydee.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, ""),
            os.path.join(BASE_DIR, "core/templates"),
            os.path.join(BASE_DIR, "shop/templates"),
            os.path.join(BASE_DIR, "shop/templates/components"),
            os.path.join(BASE_DIR, "fashion/templates/components"),
            os.path.join(BASE_DIR, "users/templates/staff"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context.core',
                'shop.context.product',
                'myadmin.context.core'
            ],
        },
    },
]

TEMPLATES[0]['OPTIONS']['debug'] = True


WSGI_APPLICATION = 'stylezbydee.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


if DEBUG:
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

else:


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
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]


LOGIN_REDIRECT_URL = 'login-redirect'

LOGOUT_REDIRECT_URL = 'home'
STATIC_URL = '/static/'

#FOR CLOUDINARY 
#email - info@stylezbydee.com
#password - V&lop!#GoikB82k 


#TAWKTO
#EMAIL = info@stylezbydee.com
#PASSWORD = V&lop!#GoikB82k


# EMAIL FOR ZOHO
EMAIL_HOST = "smtp.zoho.com"
EMAIL_PORT = "587"
# for other emails
EMAIL_HOST_USER = "customer.care@stylezbydee.com"
DEFAULT_FROM_EMAIL = "customer.care@stylezbydee.com"
EMAIL_HOST_PASSWORD = 'V&lop!#GoikB82k'
EMAIL_HOST_USER_LOGISTICS = "logistics@stylezbydee.com"
EMAIL_HOST_USER_SUPPORT = "customer.care@stylezbydee.com"

EMAIL_USE_TLS = "True"

SITE_NAME = "stylezbydee"
SITE_ADDRESS = "https://www.stylezbydee.com/"

STATIC_ROOT = os.path.join(BASE_DIR, "asset")

STATIC_URL = '/static/'
#STATICFILES_STORAGE = 'stylezbydee.storages.CustomStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'
 


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


TWILIO_ACCOUNT_SID = "AC83ee2b571fb8661d88f8c8f005ed16a1"
TWILIO_AUTH_TOKEN = "51774102535b6636a3bc21b43190bfc3"
TWILIO_PHONE_NUMBER = "+16678437916"  # Twilio SMS number
TWILIO_WHATSAPP_NUMBER = "+14155238886"  # Twilio sandbox number for WhatsApp

TWILIO_RECOVERY_CODE = "E8CEX67B36KDVFT5FC8QXZBR"

