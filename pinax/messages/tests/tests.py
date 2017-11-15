import os

# from django.conf import settings
from django.template import Context, Template
from django.test import override_settings

from ..forms import NewMessageForm, NewMessageFormMultiple
from ..hooks import hookset
from ..models import Message, Thread
from .test import TestCase


class TestCaseMixin(object):

    def assert_renders(self, tmpl, context, value):
        tmpl = Template(tmpl)
        self.assertEqual(tmpl.render(context).strip(), value)


class BaseTest(TestCase, TestCaseMixin):
    def setUp(self):
        self.brosner = self.make_user("brosner")
        self.jtauber = self.make_user("jtauber")


class TestMessages(BaseTest):
    def test_message_methods(self):
        """
        Test Message and Thread methods.
        """
        message_string = "You can't be serious"
        Message.new_message(
            self.brosner, [self.jtauber], "Really?", message_string)

        self.assertEqual(Thread.inbox(self.brosner).count(), 0)
        self.assertEqual(Thread.inbox(self.jtauber).count(), 1)
        self.assertEqual(Thread.unread(self.jtauber).count(), 1)

        thread = Thread.inbox(self.jtauber)[0]

        Message.new_reply(thread, self.jtauber, "Yes, I am.")

        self.assertEqual(Thread.inbox(self.brosner).count(), 1)
        # Replier's inbox count is unchanged but unread is decremented.
        self.assertEqual(Thread.inbox(self.jtauber).count(), 1)
        self.assertEqual(Thread.unread(self.jtauber).count(), 0)

        Message.new_reply(thread, self.brosner, "If you say so...")
        reply_string = "Indeed I do"
        Message.new_reply(thread, self.jtauber, reply_string)

        self.assertEqual(
            Thread.objects.get(pk=thread.pk).latest_message.content,
            reply_string)
        self.assertEqual(
            Thread.objects.get(pk=thread.pk).first_message.content,
            message_string)

    def test_ordered(self):
        """
        Ensure Thread ordering is last-sent-first (LIFO).
        """
        t1 = Message.new_message(
            self.brosner, [self.jtauber], "Subject",
            "A test message").thread
        t2 = Message.new_message(
            self.brosner, [self.jtauber], "Another",
            "Another message").thread
        t3 = Message.new_message(
            self.brosner, [self.jtauber], "Pwnt",
            "Haha I'm spamming your inbox").thread
        self.assertEqual(Thread.ordered([t2, t1, t3]), [t3, t2, t1])


@override_settings(
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["%s/templates" % os.path.abspath(os.path.dirname(__file__))],
            "APP_DIRS": False,
            "OPTIONS": {
                "debug": True,
                "context_processors": [
                    "django.contrib.auth.context_processors.auth",
                    "pinax_theme_bootstrap.context_processors.theme",
                    "pinax.messages.context_processors.user_messages",
                ]
            }
        },
    ]
)
class TestMessageViews(BaseTest):
    template_dirs = [
        os.path.join(os.path.dirname(__file__), "templates")
    ]

    def test_get_inbox(self):
        """
        Ensure message content appears in inbox.
        """
        message_string = "Avast ye landlubbers"
        Message.new_message(
            self.brosner, [self.jtauber], "Anything", message_string)
        with self.login(self.jtauber):
            response = self.get("pinax_messages:inbox")
            self.assertContains(response, message_string)

    def test_get_message_create(self):
        """
        Ensure user can get page to create a message.
        """
        with self.login(self.brosner):
            response = self.get("pinax_messages:message_create")
            self.assertEqual(response.status_code, 200)

    def test_post_message_create(self):
        """
        Ensure proper inbox counts when a message is sent.
        """
        with self.login(self.brosner):
            data = {
                "subject": "The internet is down.",
                "content": "Does this affect any of our sites?",
                "to_user": str(self.jtauber.id)
            }
            response = self.post("pinax_messages:message_create", data=data)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Thread.inbox(self.jtauber).count(), 1)
            self.assertEqual(Thread.inbox(self.brosner).count(), 0)

    def test_get_message_user_create(self):
        """
        Ensure form selects correct message recipient.
        """
        with self.login(self.brosner):
            response = self.get("pinax_messages:message_user_create", user_id=self.jtauber.id)
            self.assertEqual(response.status_code, 200)
            # Django v1.11+ use HTML5 boolean syntax, i.e.
            # <option value="2" selected>jtauber</option>
            #    versus XHTML syntax:
            # <option value="2" selected="selected">jtauber</option>
            regex = b"selected(\")*>jtauber</option>"
            try:
                self.assertRegex(self.last_response.content, regex)
            except AttributeError:
                self.assertRegexpMatches(self.last_response.content, regex)

    def test_sender_get_thread_detail(self):
        """
        Ensure message sender can view thread detail.
        """
        message_string = "Avast ye landlubbers"
        Message.new_message(
            self.brosner, [self.jtauber], "Anything", message_string)

        thread_id = Thread.inbox(self.jtauber).get().id
        with self.login(self.brosner):
            response = self.get("pinax_messages:thread_detail", pk=thread_id)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, message_string)

    def test_recipient_get_thread_detail(self):
        """
        Ensure message recipient can view thread detail.
        """
        message_string = "Avast ye landlubbers"
        Message.new_message(
            self.brosner, [self.jtauber], "Anything", message_string)

        thread_id = Thread.inbox(self.jtauber).get().id
        with self.login(self.jtauber):
            response = self.get("pinax_messages:thread_detail", pk=thread_id)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, message_string)

    def test_post_thread_delete(self):
        """
        Ensure a thread can be deleted by the recipient.
        """
        Message.new_message(
            self.brosner, [self.jtauber], "Anything", "and everything")

        thread_id = Thread.inbox(self.jtauber).get().id
        with self.login(self.jtauber):
            response = self.post("pinax_messages:thread_delete", pk=thread_id)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Thread.inbox(self.jtauber).count(), 0)

    def test_post_thread_detail(self):
        """
        Ensure by replying to a message the thread is marked as read.
        """
        data = {
            "content": "Nope, the internet being down doesn't affect us.",
        }
        Message.new_message(
            self.brosner, [self.jtauber], "Anything", "and everything")
        # jtauber has one unread message
        self.assertEqual(Thread.unread(self.jtauber).count(), 1)

        thread_id = Thread.inbox(self.jtauber).get().id
        with self.login(self.jtauber):
            # jtauber replies to the message...
            response = self.post("pinax_messages:thread_detail", pk=thread_id, data=data)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Thread.inbox(self.brosner).count(), 1)
            self.assertEqual(
                Thread.inbox(self.brosner).get().messages.count(),
                2
            )
            # ...and by replying implies the original message was read.
            self.assertEqual(Thread.unread(self.jtauber).count(), 0)


class TestTemplateTags(BaseTest):
    def test_unread(self):
        """
        Ensure `unread` template_tag produces correct results.
        """
        thread = Message.new_message(
            self.brosner,
            [self.jtauber],
            "Why did you break the internet?", "I demand to know.").thread
        tmpl = """
               {% load pinax_messages_tags %}
               {% if thread|unread:user %}UNREAD{% else %}READ{% endif %}
               """
        self.assert_renders(
            tmpl,
            Context({"thread": thread, "user": self.jtauber}),
            "UNREAD"
        )
        self.assert_renders(
            tmpl,
            Context({"thread": thread, "user": self.brosner}),
            "READ",
        )

    def test_unread_thread_count_one_unread(self):
        """
        Ensure `unread_threads` template_tag produces correct results for one unread message
        """
        Message.new_message(
            self.brosner,
            [self.jtauber],
            "Why did you break the internet?", "I demand to know.").thread

        tmpl = """
               {% load pinax_messages_tags %}
               {% if user|unread_thread_count %}{{ user|unread_thread_count }}{% endif %}
               """
        self.assert_renders(
            tmpl,
            Context({"user": self.jtauber}),
            "1"
        )

    def test_unread_thread_count_two_messages_incl_reply(self):
        """
        Ensure `unread_threads` template_tag produces correct results.
        """
        thread = Message.new_message(
            self.brosner,
            [self.jtauber],
            "Why did you break the internet?", "I demand to know.").thread

        Message.new_reply(thread, self.jtauber, "Replying to the first message")
        Message.new_reply(thread, self.brosner, "Replying again, so that there are two unread messages on one thread")

        Message.new_message(
            self.brosner,
            [self.jtauber],
            "Second message", "So there are two.").thread
        tmpl = """
               {% load pinax_messages_tags %}
               {% if user|unread_thread_count %}{{ user|unread_thread_count }}{% endif %}
               """
        self.assert_renders(
            tmpl,
            Context({"user": self.jtauber}),
            "2"
        )

    def test_unread_thread_count_with_all_messages_read(self):
        """
        Ensure `unread_threads` template_tag produces correct results.
        """
        thread = Message.new_message(
            self.brosner,
            [self.jtauber],
            "Why did you break the internet?", "I demand to know.").thread

        Message.new_reply(thread, self.jtauber, "Replying to the message so that I have no unread Threads")

        tmpl = """
               {% load pinax_messages_tags %}
               {{ user|unread_thread_count }}
               """
        self.assert_renders(
            tmpl,
            Context({"user": self.jtauber}),
            "0"
        )

    def test_unread_thread_count_within_with_assignment(self):
        """
        Ensure `unread_threads` template_tag produces correct results
        for one unread message when value is assigned within a {% with ... %} block.
        """
        Message.new_message(
            self.brosner,
            [self.jtauber],
            "Why did you break the internet?", "I demand to know.").thread

        tmpl = """
               {% load pinax_messages_tags %}
               {% with user|unread_thread_count as user_unread %}
               {% if user_unread %}{{ user_unread }}{% endif %}
               {% endwith %}
               """
        self.assert_renders(
            tmpl,
            Context({"user": self.jtauber}),
            "1"
        )


class TestHookSet(BaseTest):
    def test_get_user_choices(self):
        """
        Ensure all users are returned except for self
        """
        with self.assertRaises(TypeError):
            hookset.get_user_choices()

        user_choices = hookset.get_user_choices(self.brosner)
        self.assertEqual(len(user_choices), 1)
        self.assertNotIn(self.brosner, user_choices)
        self.assertIn(self.jtauber, user_choices)

        vleong = self.make_user("vleong")
        user_choices = hookset.get_user_choices(vleong)
        self.assertEqual(len(user_choices), 2)
        self.assertNotIn(vleong, user_choices)
        self.assertIn(self.brosner, user_choices)
        self.assertIn(self.jtauber, user_choices)


class TestForms(BaseTest):

    def test_new_message_form(self):
        """Verify form instantiation without a hookset for `to_user` queryset"""
        NewMessageForm(user=self.jtauber, initial={"to_user": self.brosner.pk})

    def test_new_message_form_multiple(self):
        """Verify form instantiation without a hookset for `to_user` queryset"""
        self.paltman = self.make_user("paltman")
        NewMessageFormMultiple(user=self.jtauber, initial={"to_user": [self.brosner.pk, self.paltman.pk]})
