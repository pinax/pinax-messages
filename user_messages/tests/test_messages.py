from django.contrib.auth.models import User
from django.test import TestCase

from user_messages.models import Thread, Message


class TestMessages(TestCase):
    def test_messages(self):
        brosner = User.objects.create_user('brosner', 'brosner@brosner.brosner', '')
        jtauber = User.objects.create_user('jtauber', 'jtauber@jtauber.jtauber', '')
        
        Message.objects.new_message(brosner, [jtauber], 'Really?', "You can't be serious")
        
        self.assertEqual(Thread.objects.inbox(brosner).count(), 0)
        self.assertEqual(Thread.objects.inbox(jtauber).count(), 1)
        
        Message.objects.new_reply(Thread.objects.inbox(jtauber)[0], jtauber, 'Yes, I am.')
        
        self.assertEqual(Thread.objects.inbox(brosner).count(), 1)
        self.assertEqual(Thread.objects.inbox(jtauber).count(), 1)
