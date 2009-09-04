from django.db import models


class MessageManager(models.Manager):
    def inbox(self, user):
        return self.fitler(to_user=user, deleted=False)
    
    def thread(self, message_id):
        """
        Returns all the messages in the Thread for a given message.
        """
        msg = self.select_related('thread').get(pk=message_id)
        return msg.thread.messages.all()
