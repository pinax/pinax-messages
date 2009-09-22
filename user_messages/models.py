from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from user_messages.managers import ThreadManager, MessageManager
from user_messages.utils import cached_attribute

class Thread(models.Model):
    subject = models.CharField(max_length=150)
    
    users = models.ManyToManyField(User, through='UserThread')
    
    objects = ThreadManager()
    
    @models.permalink
    def get_absolute_url(self):
        return ('messages_message_lightbox', (self.id,))
    
    @property
    @cached_attribute
    def latest_message(self):
        return self.messages.all()[0]


class UserThread(models.Model):
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(User)
    
    unread = models.BooleanField()
    deleted = models.BooleanField()


class Message(models.Model):
    thread = models.ForeignKey(Thread, related_name="messages")
    
    sender = models.ForeignKey(User, related_name="sent_messages")
    sent_at = models.DateTimeField(default=datetime.now)

    content = models.TextField()
    
    objects = MessageManager()
    
    class Meta:
        ordering = ('-sent_at',)
    
    @models.permalink
    def get_absolute_url(self):
        return ('messages_message_lightbox', (self.thread_id,))
