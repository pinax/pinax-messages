from django import get_version as get_django_version
from django.dispatch import Signal


if get_django_version() < "4":
    message_sent = Signal(providing_args=["message", "thread", "reply"])
else:
    message_sent = Signal()
