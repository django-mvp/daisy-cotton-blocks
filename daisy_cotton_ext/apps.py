"""The Django app configuration for the package."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DaisyCottonExtConfig(AppConfig):
    """Register the package's Cotton components with a Django project."""

    name = "daisy_cotton_ext"
    label = "daisy_cotton_ext"
    verbose_name = _("Extended components and page blocks")
