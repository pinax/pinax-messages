import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from user_messages.models import Thread, Message

class BaseTest(TestCase):
    def setUp(self):
        self.brosner = User.objects.create_superuser('brosner', 
            'brosner@brosner.brosner', 'abc123')
        self.jtauber = User.objects.create_superuser('jtauber', 
            'jtauber@jtauber.jtauber', 'abc123')
        self.client.login(username='brosner', password='abc123')
        if hasattr(self, 'template_dirs'):
            self._old_template_dirs = settings.TEMPLATE_DIRS
            settings.TEMPLATE_DIRS = self.template_dirs
    
    def tearDown(self):
        if hasattr(self, '_old_template_dirs'):
            settings.TEMPLATE_DIRS = self._old_template_dirs

class TestMessages(BaseTest):
    def test_messages(self):
        Message.objects.new_message(self.brosner, [self.jtauber], 'Really?', 
            "You can't be serious")
        
        self.assertEqual(Thread.objects.inbox(self.brosner).count(), 0)
        self.assertEqual(Thread.objects.inbox(self.jtauber).count(), 1)
        
        thread = Thread.objects.inbox(self.jtauber)[0]
        
        Message.objects.new_reply(thread, self.jtauber, 'Yes, I am.')
        
        self.assertEqual(Thread.objects.inbox(self.brosner).count(), 1)
        self.assertEqual(Thread.objects.inbox(self.jtauber).count(), 1)
        
        Message.objects.new_reply(thread, self.brosner, "If you say so...")
        Message.objects.new_reply(thread, self.jtauber, "Indeed I do")
        
        self.assertEqual(Thread.objects.get(pk=thread.pk).latest_message.content,
            "Indeed I do")
        self.assertEqual(Thread.objects.get(pk=thread.pk).first_message.content,
            "You can't be serious")
    
    def test_ordered(self):
        t1 = Message.objects.new_message(self.brosner, [self.jtauber], "Subject",
            "A test message").thread
        t2 = Message.objects.new_message(self.brosner, [self.jtauber], "Another",
            "Another message").thread
        t3 = Message.objects.new_message(self.brosner, [self.jtauber], "Pwnt",
            "Haha I'm spamming your inbox").thread
        self.assertEqual(Thread.ordered([t2, t1, t3]), [t3, t2, t1])

class TestMessageViews(BaseTest):
    urls = 'user_messages.tests.urls'
    template_dirs = [
        os.path.join(os.path.dirname(__file__), 'templates')
    ]
    
    def tearDown(self):
        self.client.logout()
            
    def test_create_message(self):
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('message_create'))
        self.assertEqual(response.status_code, 200)
        
        data = {
            'subject': 'The internet is down.',
            'content': 'Does this affect any of our sites?',
            'to_user': str(self.jtauber.id)
        }
        
        response = self.client.post(reverse('message_create'), data)
        self.assertEqual(response.status_code, 302)
        
        self.assertEqual(Thread.objects.inbox(self.jtauber).count(), 1)
        self.assertEqual(Thread.objects.inbox(self.brosner).count(), 0)
        
        response = self.client.get(reverse('message_create', kwargs={
            'user_id': self.jtauber.id
        }))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'selected="selected">jtauber</option>')
        
        thread_id = Thread.objects.inbox(self.jtauber).get().id
        
        response = self.client.get(reverse('thread_detail', kwargs={
            'thread_id': thread_id,
        }))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Does this affect any of our sites?')
        
        self.client.logout()
        self.client.login(username='jtauber', password='abc123')
        
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Does this affect')
        
        response = self.client.get(reverse('thread_detail', kwargs={
            'thread_id': thread_id,
        }))
        self.assertContains(response, 'Does this affect')
        
        response = self.client.post(reverse('thread_delete', kwargs={
            'thread_id': thread_id,
        }))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Thread.objects.inbox(self.jtauber).count(), 0)
        
        data = {
            'content': "Nope, the internet being down doesn't affect us.",
        }
        
        response = self.client.post(reverse('thread_detail', kwargs={
            'thread_id': thread_id,
        }), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Thread.objects.inbox(self.brosner).count(), 1)
        self.assertEqual(Thread.objects.inbox(self.brosner).get().messages.count(), 2)
