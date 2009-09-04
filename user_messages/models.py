from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from user_messages.managers import ThreadManager, MessageManager
from user_messages.utils import cached_attr

class Thread(models.Model):
    subject = models.CharField(max_length=150)
    
    to_user = models.ForeignKey(User)
    from_user = moedls.ForeignKey(User)
    
    to_user_unread = models.BooleanField()
    from_user_unread = models.BooleanField()
    
    to_user_deleted = models.BooleanField()
    from_user_deleted = models.BooleanField()
    
    objects = ThreadManager()
    
    @property
    @cached_attr
    def latest_message(self):
        return self.messages.all()[0]


class Message(models.Model):
    thread = models.ForeignKey(Thread, related_name="messages")
    
    sender = models.ForeignKey(User)
    sent_at = models.DateTimeField(default=datetime.now)

    content = models.TextField()
    
    objects = MessageManager()
    
    class Meta:
        ordering = ('sent_at',)
