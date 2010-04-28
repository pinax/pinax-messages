from django.conf.urls.defaults import *

# Any URLs that are duplicates here are to ensure we have both the correct
# version as well as the version that works with girl gamer.  Eventually we'll
# straighten GirlGamer out and fix these.

urlpatterns = patterns("user_messages.views",
    url(r"^inbox/$", "inbox", name="inbox"),
    url(r"^inbox/$", "inbox", name="messages_inbox"),
    url(r"^create/$", "message_create", name="message_create"),
    url(r"^create/(?P<user_id>\d)/$", "message_create", name="message_create"),
    url(r"^thread/(?P<thread_id>\d+)/$", "thread_detail", name="thread_detail"),
    url(r"^thread/(?P<thread_id>\d+)/$", "thread_detail", name="messages_message_lightbox"),
    url(r"^thread/(?P<thread_id>\d+)/delete/$", "thread_delete", name="thread_delete"),
)
