from django.db.models import Manager, Q


class ThreadManager(Manager):
    def inbox(self, user):
        return self.filter(Q(user_1=user, user1_deleted=False) | Q(user_2=user, user2_deleted=False))


class MessageManager(Manager):
    def new_reply(self, thread, user, content):
        msg = self.create(thread=thread, sender=user, content=content)
        if user == thread.user2:
            thread.user1_deleted = False
            thread.user1_unread = True
        else:
            thread.user2_deleted = False
            thread.user2_unread = True
        thread.save()
        return msg
    
    def new_message(self, from_user, to_user, subject, content):
        thread = Thread.objects.create(subject=subject, user1=from_user, 
            user2=to_user, user1_unread=False, user2_unread=True, 
            user1_delted=True, user2_deleted=False)
        return self.create(thread=thread, sender=from_user, content=content)
