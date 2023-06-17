
from pathlib import Path
import dj_database_url
import firebase_admin
from firebase_admin import credentials
import os
import cloudinary


# Initialize Firebase Admin SDK
cred = credentials.Certificate(
    'icuproject-d207a-firebase-adminsdk-21d15-a9c0ae1f58.json')
firebase_admin.initialize_app(cred)


FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAApTg6cnU:APA91bE89jEL80Z_EsialyBsefKEHNtsCGM7FKBkJg4o5zByM2MA755HaaVJbqTtAnQeg-3DjZoacv22XDGcFFaZspWIZqWzp-HI83FbzlbYxaEhENowveeVjniqzGaB0eLA4g1cF9zb",
    "DEFAULT_FIREBASE_APP": None,
    "APP_VERBOSE_NAME": "IcuProject",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-_)qww8fc*o&!^mmvet()__tp4hef7matki(+$)l_k&2=(r$q#1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # installed apps
    'users',
    'reports',
    'notification',
    'medicine',
    'rays',
    'medical_test',

    # external installed apps
    'rest_framework',
    'rest_framework.authtoken',
    "corsheaders",
    "phonenumber_field",
    "debug_toolbar",
    'fcm_django',
]

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

}


CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'icu2',
        'USER': 'mohamed',
        'PASSWORD': '722072207220',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

DATABASES['default'] = dj_database_url.parse(
    'postgres://icu_bgn1_user:32rSkAlzfY1bj93kDd7n3DhXEYc7gmfg@dpg-ch0rn433cv203bt3ndgg-a.oregon-postgres.render.com/icu_bgn1',
    conn_max_age=600,
    conn_health_checks=True,
)


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'ma722072207220@gmail.com'
EMAIL_HOST_PASSWORD = 'motazhtuhiyrgtuh'

AUTH_USER_MODEL = 'users.User'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_URL = '/static/'


cloudinary.config(
    cloud_name="dvm8x5hoj",
    api_key="822426192475865",
    api_secret="uHIZLfwelTRkUURkYrjBp-No7_c",
    secure=True
)
