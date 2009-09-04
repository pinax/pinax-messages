from nose.tools import assert_equal

from django.contrib.auth.models import User

from user_messages.models import Thread, Message


def test_inbox():
    brosner = User.objects.create_user('brosner', 'brosner@brosner.brosner', '')
    jtauber = User.objects.create_user('jtauber', 'jtauber@jtauber.jtauber', '')
    
    Message.objects.new_message(brosner, [jtauber], 'Really?', "You can't be serious")
    
    assert_equal(Thread.objects.inbox(brosner).count(), 0)
    assert_equal(Thread.objects.inbox(jtauber).count(), 1)
    
    Message.objects.new_reply(Thread.objects.inbox(jtauber)[0], jtauber, 'Yes, I am.')
    
    assert_equal(Thread.objects.inbox(brosner).count(), 1)
    assert_equal(Thread.objects.inbox(jtauber).count(), 1)
