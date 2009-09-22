from django.db.models import Manager, Q


class ThreadManager(Manager):
    def inbox(self, user):
        return self.filter(userthread__user=user, userthread__deleted=False)
    
    def unread(self, user):
        return self.filter(userthread__user=user, userthread__deleted=False, userthread__unread=True)


class MessageManager(Manager):
    def new_reply(self, thread, user, content):
        msg = self.create(thread=thread, sender=user, content=content)
        thread.userthread_set.exclude(user=user).update(deleted=False, unread=True)
        return msg
    
    def new_message(self, from_user, to_users, subject, content):
        from user_messages.models import Thread
        thread = Thread.objects.create(subject=subject)
        for user in to_users:
            thread.userthread_set.create(user=user, deleted=False, unread=True)
        thread.userthread_set.create(user=from_user, deleted=True, unread=False)
        return self.create(thread=thread, sender=from_user, content=content)
