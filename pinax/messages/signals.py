from django import get_version
from django.dispatch import Signal


if get_version() <= "3":
    message_sent = Signal(providing_args=["message", "thread", "reply"])
else:
    message_sent = Signal()
