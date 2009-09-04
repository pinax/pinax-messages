from django.db.models import Manager, Q


class ThreadManager(Manager):
    def inbox(self, user):
        return self.filter(Q(to_user=user, to_user_deleted=False) | Q(from_user=user, from_user_deleted=False))


class MessageManager(Manager):
    def new_reply(self, thread, user, content):
        msg = self.create(thread=thread, sender=user, content=content)
        if user == thread.from_user:
            thread.from_user_deleted = False
            thread.from_user_unread = True
        else:
            thread.to_user_deleted = False
            thread.to_user_unread = True
        thread.save()
        return msg
    
    def new_message(self, from_user, to_user, subject, content):
        thread = Thread.objects.create(subject=subject, from_user=from_user, 
            to_user=to_user, from_user_unread=False, to_user_unread=True, 
            from_user_deleted=True, to_user_deleted=False)
        return self.create(thread=thread, sender=from_user, content=content)
