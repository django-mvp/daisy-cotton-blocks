"""Django settings for testing daisy-cotton-blocks."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-test-key-for-daisy-cotton-blocks-tests-only"

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]

# Borrowed from the demo so the suite renders the pages the demo serves. The app
# order is load-bearing: the demo owns `base.html` only while "example" is above "mvp".
from example.settings import (  # noqa: E402
    EASY_ICONS,
    FLEX_MENUS,
    MVP_CONFIG,
)
from example.settings import INSTALLED_APPS as DEMO_INSTALLED_APPS  # noqa: E402

# Less the component gallery, whose startup notice would land in every test run.
INSTALLED_APPS = [app for app in DEMO_INSTALLED_APPS if app != "django_cotton_gallery"]

__all__ = ["EASY_ICONS", "FLEX_MENUS", "INSTALLED_APPS", "MVP_CONFIG"]

# Not borrowed: the demo's browser-reload middleware rewrites the response body.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "example.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "tests" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "mvp.context_processors.mvp_config",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CRISPY_ALLOWED_TEMPLATE_PACKS = ["tailwind"]
CRISPY_TEMPLATE_PACK = "tailwind"

STATIC_URL = "/static/"

USE_TZ = True
USE_I18N = True
LANGUAGE_CODE = "en-us"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
