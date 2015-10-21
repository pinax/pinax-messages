from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    "",
    url(r"^inbox/$", views.inbox, name="messages_inbox"),
    url(r"^create/$", views.message_create, name="message_create"),
    url(r"^create/(?P<user_id>\d+)/$", views.message_create, name="message_create"),
    url(r"^thread/(?P<thread_id>\d+)/$", views.thread_detail, name="messages_thread_detail"),
    url(r"^thread/(?P<thread_id>\d+)/delete/$", views.thread_delete, name="messages_thread_delete"),
)
