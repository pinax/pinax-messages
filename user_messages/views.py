from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST

from user_messages.forms import MessageReplyForm, NewMessageForm
from user_messages.models import Thread, Message


@login_required
def inbox(request, template_name='user_messages/inbox.html'):
    threads = list(Thread.objects.inbox(request.user))
    threads.sort(key=lambda o: o.latest_message.sent_at, reverse=True)
    return render_to_response(template_name, {'threads': threads}, context_instance=RequestContext(request))


@login_required
def thread_detail(request, thread_id, 
    template_name='user_messages/thread_detail.html'):
    qs = Thread.objects.filter(userthread__user=request.user)
    thread = get_object_or_404(qs, pk=thread_id)
    if request.method == 'POST':
        form = MessageReplyForm(request.POST, user=requst.user, thread=thread)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(inbox))
    else:
        form = MessageReplyForm(user=request.user, thread=thread)
        thread.userthread_set.filter(user=request.user).update(unread=False)
    return render_to_response(template_name, {
        'thread': thread,
        'form': form
    }, context_instance=RequestContext(request))


@login_required
def message_create(request, user_id=None, 
    template_name='user_messages/message_create.html'):
    if user_id is not None:
        user_id = int(user_id)
    initial = {'to_user': user_id}
    if request.method == 'POST':
        form = NewMessageForm(request.POST, user=request.user, initial=initial)
        if form.is_valid():
            msg = form.save()
            return HttpResponseRedirect(msg.get_absolute_url())
    else:
        form = NewMessageForm(user=request.user, initial=initial)
    return render_to_response(template_name, {
        'form': form
    }, context_instance=RequestContext(request))


@login_required
@require_POST
def thread_delete(request, thread_id):
    qs = Thread.objects.filter(userthread__user=request.user)
    thread = get_object_or_404(qs, pk=thread_id)
    thread.userthread_set.filter(user=request.user).update(delted=True)
    return HttpResponseRedirect(reverse(inbox))
