from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    TemplateView,
    UpdateView
)

from .forms import MessageReplyForm, NewMessageForm, NewMessageFormMultiple
from .models import Thread

try:
    from account.decorators import login_required
except:  # noqa
    from django.contrib.auth.decorators import login_required


class InboxView(TemplateView):
    """
    View inbox thread list.
    """
    template_name = "pinax/messages/inbox.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InboxView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InboxView, self).get_context_data(**kwargs)
        if self.kwargs.get("deleted", None):
            threads = Thread.ordered(Thread.deleted(self.request.user))
            folder = "deleted"
        else:
            threads = Thread.ordered(Thread.inbox(self.request.user))
            folder = "inbox"

        context.update({
            "folder": folder,
            "threads": threads,
            "threads_unread": Thread.ordered(Thread.unread(self.request.user))
        })
        return context


class ThreadView(UpdateView):
    """
    View a single Thread or POST a reply.
    """
    model = Thread
    form_class = MessageReplyForm
    context_object_name = "thread"
    template_name = "pinax/messages/thread_detail.html"
    success_url = reverse_lazy("pinax_messages:inbox")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadView, self).dispatch(*args, **kwargs)

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

    def get(self, request, *args, **kwargs):
        response = super(ThreadView, self).get(request, *args, **kwargs)
        self.object.userthread_set.filter(user=request.user).update(unread=False)
        return response


class MessageCreateView(CreateView):
    """
    Create a new thread message.
    """
    template_name = "pinax/messages/message_create.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MessageCreateView, self).dispatch(*args, **kwargs)

    def get_form_class(self):
        if self.form_class is None:
            if self.kwargs.get("multiple", False):
                return NewMessageFormMultiple
        return NewMessageForm

    def get_initial(self):
        user_id = self.kwargs.get("user_id", None)
        if user_id is not None:
            user_id = [int(user_id)]
        elif "to_user" in self.request.GET and self.request.GET["to_user"].isdigit():
            user_id = map(int, self.request.GET.getlist("to_user"))
        if not self.kwargs.get("multiple", False) and user_id:
            user_id = user_id[0]
        return {"to_user": user_id}

    def get_form_kwargs(self):
        kwargs = super(MessageCreateView, self).get_form_kwargs()
        kwargs.update({
            "user": self.request.user,
        })
        return kwargs


class ThreadDeleteView(DeleteView):
    """
    Delete a thread.
    """
    model = Thread
    success_url = reverse_lazy("pinax_messages:inbox")
    template_name = "pinax/messages/thread_confirm_delete.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.userthread_set.filter(user=request.user).update(deleted=True)
        return HttpResponseRedirect(success_url)
