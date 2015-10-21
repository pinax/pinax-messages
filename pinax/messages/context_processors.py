from .models import Thread


def user_messages(request):
    c = {}
    if request.user.is_authenticated():
        c["inbox_count"] = Thread.inbox(request.user).count()
    return c
