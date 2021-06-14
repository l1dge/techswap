from decouple import config, Csv
import dj_database_url
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


DATABASES = {"default": dj_database_url.config(default=config("DATABASE_URL"))}

SECRET_KEY = config("SECRET_KEY")


DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "swapshop.apps.SwapshopConfig",
    "storages",
    "location_field.apps.DefaultConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "TechSwap.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "TechSwap.wsgi.application"

AUTH_USER_MODEL = "swapshop.AppUser"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = config("LOGIN_URL")
LOGIN_REDIRECT_URL = config("LOGIN_REDIRECT_URL")

# Used for testing email, logs to console.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST")
EMAIL_USE_TLS = config("EMAIL_USE_TLS")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")


# Amazon S3 credentials
FILE_URL = config("FILE_URL")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# Google Map Settings
LOCATION_FIELD_PATH = STATIC_URL + "location_field"
LOCATION_FIELD = {
    "map.provider": "google",
    "map.zoom": 13,
    "search.provider": "google",
    "search.suffix": "",
    # Google
    "provider.google.api": "//maps.google.com/maps/api/js?sensor=false",
    "provider.google.api_key": config("LOCATION_API_KEY"),
    "provider.google.api_libraries": "",
    "provider.google.map.type": "ROADMAP",
}
LOCATION_API_KEY = config("LOCATION_API_KEY")

SITE_ID = 1


# debugging
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#     },
#     "root": {
#         "handlers": ["console"],
#         "level": "DEBUG",
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["console"],
#             "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
#             "propagate": False,
#         },
#     },
# }
