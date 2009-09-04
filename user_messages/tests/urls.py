from django.conf.urls.defaults import *

urlpatterns = patterns('user_messages.views',
    url(r'^inbox/$', 'inbox', name='inbox'),
    url(r'^create/$', 'message_create', name='message_create'),
    url(r'^thread/(?P<thread_id>\d+)/$', 'thread_detail', name='thread_detail'),
)
