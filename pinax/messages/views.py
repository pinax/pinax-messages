from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormMixin
from django.views.decorators.http import require_POST

from account.decorators import login_required
from account.mixins import LoginRequiredMixin

from .forms import MessageReplyForm, NewMessageForm, NewMessageFormMultiple
from .models import Thread


class InboxView(LoginRequiredMixin, TemplateView):
    template_name = "pinax/messages/inbox.html"

    def get_context_data(self, **kwargs):
        context = super(InboxView, self).get_context_data(**kwargs)
        context.update({
            "threads": Thread.ordered(Thread.inbox(self.request.user)),
            "threads_unread": Thread.ordered(Thread.unread(self.request.user))
        })
        return context


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    model = Thread
    context_object_name = "thread"
    template_name = "pinax/messages/thread_detail.html"
    form_class = MessageReplyForm

    def get_queryset(self):
        qs = super(ThreadView, self).get_queryset()
        qs = qs.filter(userthread__user=self.request.user).distinct()
        return qs

    def get_form_kwargs(self):
        kwargs = super(ThreadView, self).get_form_kwargs()
        kwargs.update({
            "user": self.request.user,
            "thread": self.object
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context.update({
            "form": self.get_form()
        })
        return context

    def get_success_url(self):
        return reverse("messages_inbox")

    def get(self, request, *args, **kwargs):
        response = super(ThreadView, self).get(request, *args, **kwargs)
        self.object.userthread_set.filter(user=request.user).update(unread=False)
        return response

    def form_valid(self, form):
        form.save()
        return super(ThreadView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def message_create(
    request, user_id=None,
    template_name="user_messages/message_create.html",
    form_class=None, multiple=False
):
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
