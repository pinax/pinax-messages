from .models import Thread


def user_messages(request):
    c = {}
    if request.user.is_authenticated():
        c["inbox_threads"] = Thread.inbox(request.user)
        c["unread_threads"] = Thread.unread(request.user)
    return c
