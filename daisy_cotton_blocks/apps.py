"""The Django app configuration for the package."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DaisyCottonBlocksConfig(AppConfig):
    """Register the package's Cotton components with a Django project."""

    name = "daisy_cotton_blocks"
    label = "daisy_cotton_blocks"
    verbose_name = _("Page blocks")
