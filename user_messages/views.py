from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required

from user_messages.forms import MessageReplyForm, NewMessageForm, NewMessageFormMultiple
from user_messages.models import Thread


@login_required
def inbox(request, template_name="user_messages/inbox.html"):
    threads = Thread.ordered(Thread.objects.inbox(request.user))
    return render_to_response(template_name, {
        "threads": threads
    }, context_instance=RequestContext(request))


@login_required
def thread_detail(request, thread_id,
    template_name="user_messages/thread_detail.html",
    form_class=MessageReplyForm):
    qs = Thread.objects.filter(userthread__user=request.user).distinct()
    thread = get_object_or_404(qs, pk=thread_id)
    if request.method == "POST":
        form = form_class(request.POST, user=request.user, thread=thread)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("messages_inbox"))
    else:
        form = form_class(user=request.user, thread=thread)
        thread.userthread_set.filter(user=request.user).update(unread=False)
    return render_to_response(template_name, {
        "thread": thread,
        "form": form
    }, context_instance=RequestContext(request))


@login_required
def message_create(request, user_id=None,
    template_name="user_messages/message_create.html",
    form_class=None, multiple=False):
    if form_class is None:
        if multiple:
            form_class = NewMessageFormMultiple
        else:
            form_class = NewMessageForm
    
    if user_id is not None:
        user_id = [int(user_id)]
    elif "to_user" in request.GET and request.GET["to_user"].isdigit():
        user_id = map(int, request.GET.getlist("to_user"))
    if not multiple and user_id:
        user_id = user_id[0]
    initial = {"to_user": user_id}
    if request.method == "POST":
        form = form_class(request.POST, user=request.user, initial=initial)
        if form.is_valid():
            msg = form.save()
            return HttpResponseRedirect(msg.get_absolute_url())
    else:
        form = form_class(user=request.user, initial=initial)
    return render_to_response(template_name, {
        "form": form
    }, context_instance=RequestContext(request))


@login_required
@require_POST
def thread_delete(request, thread_id):
    qs = Thread.objects.filter(userthread__user=request.user)
    thread = get_object_or_404(qs, pk=thread_id)
    thread.userthread_set.filter(user=request.user).update(deleted=True)
    return HttpResponseRedirect(reverse("messages_inbox"))
