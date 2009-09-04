from django.conf.urls.defaults import *

urlpatterns = patterns('user_messages.views',
    url(r'^inbox/$', 'inbox', name='inbox'),
)
