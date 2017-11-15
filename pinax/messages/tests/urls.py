from django.conf.urls import include, url

urlpatterns = [
    url(r"^", include("pinax.messages.urls", namespace="pinax_messages")),
]
