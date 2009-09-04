from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from user_messages.managers import MessageManager

class Thread(models.Model):
    subject = models.CharField(max_length=150)

class Message(models.Model):
    thread = models.ForeignKey(Thread)
    
    from_user = models.ForeignKey(User, related_name="messages_sent")
    to_user = models.ForeignKey(User, related_name="messagses_received")
    
    sent_at = models.DateTimeField(default=datetime.now)
    
    reply_to = models.ForeignKey('self', null=True, related_name='replies')
    
    content = models.TextField()
    
    # this refers to whether the to_user has read this message, the from_user 
    # has always read the messages they sent
    unread = models.BooleanField(default=True)
    # again, this field is exclusively for a to_user, a from_user can't delete 
    # a message they sent from their inbox since it was never there.
    deleted = models.BooealField(default=False)
    
    objects = MessageManager()
    
    class Meta:
        ordering = ('sent_at',)
