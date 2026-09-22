"""Django settings for testing daisy-cotton-blocks."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-test-key-for-daisy-cotton-blocks-tests-only"

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]

# Borrowed from the demo rather than restated. The suite renders the demo's own
# pages, so a second copy of its app list, icons, menus and shell configuration
# here would be a second thing to keep true, and the copy that drifts is always
# the one nobody is reading when a page mysteriously stops rendering.
#
# The app list matters most of all, because its order is load-bearing: the demo
# owns the unqualified `base.html` only while "example" sits above "mvp", and a
# second list that puts them the other way round renders the suite a page the
# browser never serves.
from example.settings import (  # noqa: E402
    EASY_ICONS,
    FLEX_MENUS,
    MVP_CONFIG,
)
from example.settings import INSTALLED_APPS as DEMO_INSTALLED_APPS  # noqa: E402

# Everything the demo installs, less the component gallery. The gallery prints a
# mounted-and-serving notice from an app registry hook, which would land in every
# test run, and nothing under tests/ exercises its pages.
INSTALLED_APPS = [app for app in DEMO_INSTALLED_APPS if app != "django_cotton_gallery"]

__all__ = ["EASY_ICONS", "FLEX_MENUS", "INSTALLED_APPS", "MVP_CONFIG"]

# Not borrowed. The demo's chain ends with the middleware that rewrites a
# response to insert the browser-reload script, which has no business running
# underneath assertions about what a page contains.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# The demo's URLconf, so the catalogue views are reachable from the suite.
ROOT_URLCONF = "example.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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
