from django import template

from pinax.messages.models import Thread

register = template.Library()


@register.filter
def unread(thread, user):
    '''
    Check whether there are any unread messages for a particular thread for a user.
    '''
    return bool(thread.userthread_set.filter(user=user, unread=True))


@register.filter
def unread_threads(user):
    '''
    Return the number of unread threads for this user, useful for highlighting on an account bar for example.
    '''
    return len(Thread.unread(user))
