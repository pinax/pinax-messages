from django.dispatch import Signal

message_sent = Signal("message", "thread", "reply")
