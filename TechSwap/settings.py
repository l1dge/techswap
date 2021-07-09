from decouple import config, Csv
import dj_database_url
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


DATABASES = {"default": dj_database_url.config(default=config("DATABASE_URL"))}

SECRET_KEY = config("SECRET_KEY")


DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    "127.0.0.1",
    ".herokuapp.com",
    "glacial-sierra-78162.herokuapp.com",
]


INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
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
    "swapshop.apps.SwapshopConfig",
    "storages",
    "location_field.apps.DefaultConfig",
    "debug_toolbar",
    "django_truncate",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400  # 1 day in seconds
ACCOUNT_FORMS = {"signup": "swapshop.forms.UserRegistrationForm"}
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login/"

# Used for testing email, logs to console.
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
if DEBUG == True:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST")
EMAIL_USE_TLS = config("EMAIL_USE_TLS")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")


# Amazon S3 credentials
FILE_URL = config("FILE_URL")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = "public-read"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

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

INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

WHITENOISE_USE_FINDERS = True
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
