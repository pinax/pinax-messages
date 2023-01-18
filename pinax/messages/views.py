from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    TemplateView,
    UpdateView,
)

from .forms import MessageReplyForm, NewMessageForm
from .models import Thread


@login_required
def inbox(request: HttpRequest) -> HttpResponse:
    context = {
        "threads_all": Thread.objects.sorted_active(request.user),
        "threads_unread": Thread.objects.sorted_unread(request.user),
    }
    return render(request, "pinax/messages/inbox.html", context)


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
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(userthread__user=self.request.user).distinct()
        return qs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "user": self.request.user,
            "thread": self.object
        })
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object.userthread_set.filter(user=request.user).update(unread=False)
        return super().get(request, *args, **kwargs)


class MessageCreateView(CreateView):
    """
    Create a new thread message.
    """
    form_class = NewMessageForm
    template_name = "pinax/messages/message_create.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        user_ids = ()
        if "to_users" in self.request.GET:
            user_ids = map(int, self.request.GET.getlist("to_users"))
        return {"to_users": user_ids}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
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
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.userthread_set.filter(user=request.user).update(deleted=True)
        return HttpResponseRedirect(success_url)
