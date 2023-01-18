from typing import List

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .signals import message_sent
from .utils import cached_attribute


UserModel = get_user_model()


class ThreadManager(models.Manager):
    def _sort_threads_list(self, threads_list: List["Thread"]) -> List["Thread"]:
        return sorted(threads_list, key=lambda thread: thread.latest_message.sent_at, reverse=True)

    def unread(self, user) -> QuerySet:
        return self.filter(userthread__user=user, userthread__unread=True, userthread__deleted=False).distinct()

    def sorted_unread(self, user) -> List["Thread"]:
        unread = self.unread(user)
        return self._sort_threads_list(list(unread))

    def active(self, user) -> QuerySet:
        """All threads in which the user is involved."""
        return self.filter(userthread__user__id=user.pk, userthread__deleted=False).distinct()

    def sorted_active(self, user) -> List["Thread"]:
        active = self.active(user)
        return self._sort_threads_list(list(active))


class Thread(models.Model):
    objects = ThreadManager()

    subject = models.CharField(_("subject"), max_length=150)
    users = models.ManyToManyField(UserModel, through="UserThread", verbose_name=_("users"))

    @classmethod
    def inbox(cls, user):
        return cls.objects.filter(userthread__user=user, userthread__deleted=False)

    @classmethod
    def deleted(cls, user):
        return cls.objects.filter(userthread__user=user, userthread__deleted=True)

    def __str__(self):
        return f"{self.subject}"

    def get_absolute_url(self):
        return reverse("pinax_messages:thread_detail", args=[self.pk])

    @property
    @cached_attribute
    def first_message(self):
        return self.messages.first()

    @property
    @cached_attribute
    def latest_message(self):
        return self.messages.order_by("-sent_at").first()

    @property
    def num_messages(self):
        return self.messages.count()

    @property
    def num_users(self):
        """Total number of users registered to this thread"""
        return self.users.count()

    @classmethod
    def ordered(cls, objs):
        """
        Returns the iterable ordered the correct way, this is a class method
        because we don"t know what the type of the iterable will be.
        """
        objs = list(objs)
        objs.sort(key=lambda o: o.latest_message.sent_at, reverse=True)
        return objs

    class Meta:
        verbose_name = _("thread")
        verbose_name_plural = _("threads")


class UserThread(models.Model):
    thread = models.ForeignKey("Thread", on_delete=models.CASCADE, verbose_name=_("thread"))
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("user"))
    unread = models.BooleanField(_("unread"), default=True)
    deleted = models.BooleanField(_("deleted"), default=False)

    class Meta:
        verbose_name = _("user thread")
        verbose_name_plural = _("user threads")


class MessageManager(models.Manager):
    def new_reply(self, thread, user, content):
        """
        Generate a new message for the input thread.

        Whenever a new reply is created, all the previously subscribed users will see this message in their inbox, even
        if they had previously deleted the message in the past.
        """
        msg = self.create(thread=thread, sender=user, content=content)
        thread.userthread_set.exclude(user=user).update(deleted=False, unread=True)
        thread.userthread_set.filter(user=user).update(unread=False)
        message_sent.send(sender=self.model, message=msg, thread=thread, reply=True)
        return msg

    def new_message(self, from_user, to_users, subject, content):
        """
        Create a new conversation thread and its first message.

        The new thread will involve both the `from_user` and all users from the `to_users` parameters.
        """
        thread = Thread.objects.create(subject=subject)
        thread.userthread_set.create(user=from_user, unread=False)
        for user in to_users:
            thread.userthread_set.create(user=user)
        msg = self.create(thread=thread, sender=from_user, content=content)
        message_sent.send(sender=self.model, message=msg, thread=thread, reply=False)
        return msg


class Message(models.Model):
    objects = MessageManager()

    thread = models.ForeignKey(
        "Thread",
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name=_("thread"),
    )
    sender = models.ForeignKey(
        UserModel,
        related_name="sent_messages",
        on_delete=models.CASCADE,
        verbose_name=_("sender"),
    )
    sent_at = models.DateTimeField(_("sent at"), default=timezone.now)
    content = models.TextField(_("content"))

    def get_absolute_url(self):
        return self.thread.get_absolute_url()

    class Meta:
        ordering = ("sent_at",)
        verbose_name = _("message")
        verbose_name_plural = _("messages")
