from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    "",
    url(r"^inbox/$", views.InboxView.as_view(), name="messages_inbox"),
    url(r"^create/$", views.MessageCreateView.as_view(), name="message_create"),
    url(r"^create/(?P<user_id>\d+)/$", views.MessageCreateView.as_view(), name="message_create"),
    url(r"^thread/(?P<pk>\d+)/$", views.ThreadView.as_view(), name="messages_thread_detail"),
    url(r"^thread/(?P<pk>\d+)/delete/$", views.ThreadDeleteView.as_view(), name="messages_thread_delete"),
)
