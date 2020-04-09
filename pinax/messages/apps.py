from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "pinax.messages"
    label = "pinax_messages"
    verbose_name = _("Pinax Messages")
