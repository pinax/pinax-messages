# Usage

`pinax-messages` handles user-to-user private threaded messaging primarily by the inclusion of template snippets. These snippets fall into three categories: view message inbox (all threads), view message thread, and create (or respond to) a message.

### Access Inbox

Place this snippet wherever a "Message Inbox" link is needed for viewing user message inbox:

```html
<a href="{% url 'pinax_messages:inbox' %}"><i class="fa fa-envelope"></i> {% trans "Message Inbox" %}</a>
```

### View Message Thread

Place this snippet wherever you have need to view a specific message thread:

```html
<a href="{% url 'pinax_messages:thread_detail' thread.pk %}"><i class="fa fa-envelope"></i> {% trans "View Message Thread" %}</a>
```

### Create Message - Template

Add the following line to an object template in order to provide a button for messaging a user associated with `object`:

```html
<a href="{% url "pinax_messages:message_user_create" user_id=object.user.id %}" class="btn btn-default">Message this user</a>
```

### Create Message - Code

Use the following code to create a new message programmatically. Note that `to_users` (message recipients) is a list, allowing messages sent to multiple users.

```python
from pinax.messages.models import Message

Message.new_message(from_user=self.request.user, to_users=[user], subject=subject, content=content)
```

### Template Context Variables

`pinax-messages` provides two context variables using a template context processor. In order to access these in your templates, add `user_messages` to your `TEMPLATE_CONTEXT_PROCESSORS`:

```python
TEMPLATE_CONTEXT_PROCESSORS = [
    ...
    "pinax.messages.context_processors.user_messages",
    ...
]
```

The following context variables are available, and work with the current authenticated user:

* `inbox_threads` — all message threads for current user
* `unread_threads` — unread message threads for current user

### Templates

[Example templates](https://github.com/pinax/pinax-theme-bootstrap/tree/master/pinax_theme_bootstrap/templates/pinax/messages) are available in the `pinax-theme-bootstrap` [project](https://github.com/pinax/pinax-theme-bootstrap/tree/master/pinax_theme_bootstrap).

See [Reference Guide](./reference.md) for details about URL and template names.

***
[Documentation Index](./index.md)
