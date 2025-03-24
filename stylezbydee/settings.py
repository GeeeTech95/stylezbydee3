import environ
import os
from pathlib import Path
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()  # Read the .env file

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Security settings for production
SECRET_KEY = env('DJANGO_SECRET_KEY', default='your-default-secret-key')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

SITE_WHATSAPP_NO = env('SITE_WHATSAPP_NO', default="+2348162467444")
SITE_URL = env('SITE_URL', default="http://127.0.0.1:8000")

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
    "SITE_ICON": {
        "light": lambda request: static("icon-light.svg"),  # light mode
        "dark": lambda request: static("icon-dark.svg"),  # dark mode
    },
    "SITE_LOGO": {
        "light": lambda request: static("logo-light.svg"),  # light mode
        "dark": lambda request: static("logo-dark.svg"),  # dark mode
    },
    "SITE_SYMBOL": "speed",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon.svg"),
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "THEME": "light",  # Force theme: "dark" or "light". Will disable theme switcher
    "LOGIN": {
        "image": lambda request: static("img/studio/DSC_0944.jpg"),
    },
}

JAZZMIN_SETTINGS = {
    "site_title": "StylezByDee Admin",
    "site_header": "StylezByDee",
    "site_brand": "StylezByDee",
    "site_logo": "img/logo/logo-name.png",
    "login_logo": "img/logo/icon-jazz.png",
    "login_logo_dark": "img/logo/logo-name-dark.png",
    "site_logo_classes": ["logo"],
    "custom_css": "css/style.css",
    "site_icon": "img/logo/icon-jazz.png",
    "welcome_sign": "Welcome Admin!",
    "copyright": "StylezByDee",
}

# Application definition
INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "django.contrib.admin",
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

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
}

if DEBUG:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
else:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
                'myadmin.context.core',
            ],
        },
    },
]

TEMPLATES[0]['OPTIONS']['debug'] = True

WSGI_APPLICATION = 'stylezbydee.wsgi.application'

# Database configuration using DATABASE_URL from environment variables

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

LOGIN_REDIRECT_URL = 'login-redirect'
LOGOUT_REDIRECT_URL = 'home'
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'

# Email settings using environment variables
EMAIL_HOST = env('EMAIL_HOST', default="smtp.zoho.com")
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default="customer.care@stylezbydee.com")
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)

# Twilio settings using environment variables
TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID') #added this
TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = env('TWILIO_PHONE_NUMBER')
TWILIO_WHATSAPP_NUMBER = env('TWILIO_WHATSAPP_NUMBER')
TWILIO_RECOVERY_CODE = env('TWILIO_RECOVERY_CODE')

# Site and security settings
SITE_NAME = env('SITE_NAME', default="stylezbydee")
SITE_ADDRESS = env('SITE_ADDRESS', default="https://www.stylezbydee.com/")
STATIC_ROOT = os.path.join(BASE_DIR, "asset")



# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
