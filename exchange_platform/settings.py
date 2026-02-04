import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent  # πρέπει να υπάρχει ήδη

STATICFILES_DIRS = [BASE_DIR / "static"]


SECRET_KEY = 'django-insecure-peigb@_+^o%v6s9yiu%j%j=i)bt*hvke3b(xh_f1g=tk6w@qfk'

DEBUG = True

ALLOWED_HOSTS = []



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
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

ROOT_URLCONF = 'exchange_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'exchange_platform.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Stripe (βάλε εδώ τα test keys σου από Stripe Dashboard)
STRIPE_PUBLIC_KEY = "pk_test_xxxxxxxxxxxxxxxxxxxxx"
STRIPE_SECRET_KEY = "sk_test_xxxxxxxxxxxxxxxxxxxxx"

# Price ID για το πακέτο credits (θα το φτιάξεις στο Stripe)
STRIPE_PRICE_ID = "price_xxxxxxxxxxxxx"

STRIPE_SUCCESS_URL = "http://127.0.0.1:8000/billing/success/"
STRIPE_CANCEL_URL = "http://127.0.0.1:8000/billing/cancel/"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "space_list"
LOGOUT_REDIRECT_URL = "space_list"
