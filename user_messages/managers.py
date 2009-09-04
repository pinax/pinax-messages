from django.db.models import Manager, Q

class ThreadManager(Manager):
    def inbox(self, user):
        return self.filter(Q(user_1=user, user1_deleted=False) | Q(user_2=user, user2_deleted=False))
