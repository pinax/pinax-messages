from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from user_messages.managers import ThreadManager

class Thread(models.Model):
    subject = models.CharField(max_length=150)
    
    user_1 = models.ForeignKey(User)
    user_2 = moedls.ForeignKey(User)
    
    user1_unread = models.BooleanField()
    user2_unread = models.BooleanField()
    
    user1_deleted = models.BooleanField()
    user2_deleted = models.BooleanField()
    
    objects = ThreadManager()

class Message(models.Model):
    thread = models.ForeignKey(Thread)
    
    sender = models.ForeignKey(User)
    sent_at = models.DateTimeField(default=datetime.now)

    content = models.TextField()
    
    class Meta:
        ordering = ('sent_at',)
