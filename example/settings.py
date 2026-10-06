"""Settings for the example project.

Demonstration target, never deployed. It runs on the development server so the
components can be looked at in a browser while they are being built.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-example-project-only"

DEBUG = True

# The development server is reached by hostname, and DEBUG auto-allows only
# localhost, so any other hostname would get a 400.
ALLOWED_HOSTS = ["*"]

# The development server speaks plain HTTP, where a Secure cookie is discarded
# and every form post comes back 403.
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# "example" sits above "mvp" so the demo's templates win, and "mvp" above
# "crispy_tailwind" so its help-text override wins.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # The gallery scans only the first template root with a cotton/ directory,
    # so this must stay above "example" or it would index the demo's scaffolding.
    "daisy_cotton_ext",
    "example",
    "django_cotton",
    # Development only: it serves component source, so urls.py mounts it under DEBUG.
    "django_cotton_gallery",
    "django_browser_reload",
    "easy_icons",
    "flex_menu",
    "mvp",
    # The base components this package builds on. Below "mvp", so the shell
    # keeps its own copies of the components both packages carry.
    "daisy_cotton",
    "crispy_forms",
    "crispy_tailwind",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Last, because it rewrites the response body and anything that compresses
    # the body has to run after it.
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

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

WSGI_APPLICATION = "example.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "example.sqlite3",
    }
}

CRISPY_ALLOWED_TEMPLATE_PACKS = ["tailwind"]
CRISPY_TEMPLATE_PACK = "tailwind"

FLEX_MENUS = {
    "renderers": {
        "sidebar": "mvp.renderers.SidebarRenderer",
        "dock": "mvp.renderers.MobileFooterNavRenderer",
    }
}

EASY_ICONS = {
    "default": {
        "renderer": "easy_icons.renderers.ProviderRenderer",
        "config": {"tag": "i"},
        "packs": ["mvp.utils.BS5_ICONS"],
        "icons": {
            "home": "bi bi-house",
            "block": "bi bi-square",
            "gallery": "bi bi-grid-3x3-gap",
        },
    }
}

# daisyUI's own themes, spanning light, dark and heavily tinted: a block that
# only reads on two of them is not finished.
MVP_CONFIG = {
    "theme": {
        "default": "light",
        "choices": [
            "light",
            "dark",
            "cupcake",
            "emerald",
            "corporate",
            "synthwave",
            "dracula",
            "business",
            "night",
            "winter",
        ],
    },
    "layout": {
        "sidebar": {
            "title": "daisy-cotton-ext",
            "breakpoint": "lg",
            "collapse": "icons",
        },
        "navbar": {"desktop": {"end": ["actions.theme-controller"]}},
    },
}

STATIC_URL = "/static/"

USE_TZ = True
USE_I18N = True
LANGUAGE_CODE = "en-us"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
