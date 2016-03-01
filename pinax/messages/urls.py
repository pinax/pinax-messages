from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^inbox/$", views.InboxView.as_view(),
        name="pinax_messages_inbox"),
    url(r"^create/$", views.MessageCreateView.as_view(),
        name="pinax_messages_message_create"),
    url(r"^create/(?P<user_id>\d+)/$", views.MessageCreateView.as_view(),
        name="pinax_messages_message_user_create"),
    url(r"^thread/(?P<pk>\d+)/$", views.ThreadView.as_view(),
        name="pinax_messages_thread_detail"),
    url(r"^thread/(?P<pk>\d+)/delete/$", views.ThreadDeleteView.as_view(),
        name="pinax_messages_thread_delete"),
]
