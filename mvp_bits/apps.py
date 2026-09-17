from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MvpBitsConfig(AppConfig):
    name = "mvp_bits"
    label = "mvp_bits"
    verbose_name = _("Page blocks")
