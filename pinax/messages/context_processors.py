from .models import Thread


def user_messages(request):
    context = {}
    if request.user.is_authenticated:
        context["inbox_count"] = Thread.objects.unread_threads(request.user).count()
    return context
