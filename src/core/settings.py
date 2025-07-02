import os.path
from pathlib import Path

from django.conf.global_settings import (
    MEDIA_ROOT,
    MEDIA_URL,
    STATICFILES_DIRS,
    STATIC_ROOT,
    LOGOUT_REDIRECT_URL,
)

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-sd3y9^j#$1i=ej1h=%g-ge2l9=olwnulc0-nys*!b&q+_d_wk2"

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_EXTENSIONS = [
    "common.apps.CommonConfig",
    "exercises.apps.ExercisesConfig",
    "accounts.apps.AccountsConfig",
    "analytics.apps.AnalyticsConfig",
    "groups.apps.GroupsConfig",
    "friendships.apps.FriendshipsConfig",
    "notifications.apps.NotificationsConfig",
    "training_plans.apps.TrainingPlansConfig",
    "workout_performance.apps.WorkoutPerformanceConfig",
]

INSTALLED_APPS += INSTALLED_EXTENSIONS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "common" / "templates" / "common"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "common" / "static"]

MEDIA_ROOT = BASE_DIR / "common" / "media"
MEDIA_URL = "/common/media/"

LOGIN_REDIRECT_URL = "common-home"
LOGIN_URL = "accounts-login"

LOGOUT_REDIRECT_URL = "common-home"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
