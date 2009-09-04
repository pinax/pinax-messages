from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from user_messages.models import Thread, Message

class BaseTest(TestCase):
    def setUp(self):
        self.brosner = User.objects.create_superuser('brosner', 'brosner@brosner.brosner', 'abc123')
        self.jtauber = User.objects.create_superuser('jtauber', 'jtauber@jtauber.jtauber', 'abc123')
        self.client.login(username='brosner', password='abc123')

class TestMessages(BaseTest):
    def test_messages(self):
        Message.objects.new_message(self.brosner, [self.jtauber], 'Really?', "You can't be serious")
        
        self.assertEqual(Thread.objects.inbox(self.brosner).count(), 0)
        self.assertEqual(Thread.objects.inbox(self.jtauber).count(), 1)
        
        Message.objects.new_reply(Thread.objects.inbox(self.jtauber)[0], self.jtauber, 'Yes, I am.')
        
        self.assertEqual(Thread.objects.inbox(self.brosner).count(), 1)
        self.assertEqual(Thread.objects.inbox(self.jtauber).count(), 1)

class TestMessageViews(BaseTest):
    urls = 'user_messages.tests.urls'
    
    def tearDown(self):
        self.client.logout()
            
    def test_create_message(self):
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
