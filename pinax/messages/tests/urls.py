from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("", include("pinax.messages.urls", namespace="pinax_messages")),
]
