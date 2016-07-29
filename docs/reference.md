# Reference Guide

### URL–View–Template Matrix

| URL Name                             | View                  | Template              |
| ------------------------------------ | --------------------- | --------------------- |
| `pinax-messages:inbox`               | `InboxView()`         | `inbox.html`          |
| `pinax-messages:message_create`      | `MessageCreateView()` | `message_create.html` |
| `pinax-messages:message_user_create` | `MessageCreateView()` | `message_create.html` |
| `pinax-messages:thread_detail`       | `ThreadView()`        | `thread_detail.html`  |
| `pinax-messages:thread_delete`       | `ThreadDeleteView()`  | N/A                   |

### URL Names

These URL names are available when using pinax-messages urls.py:

`pinax-messages:inbox` — Inbox view

`pinax-messages:message_create` — Create new message

`pinax-messages:message_user_create` — Create new message to specific user

`pinax-messages:thread_detail` — View message thread, requires thread PK

`pinax-messages:thread_delete` — Delete message thread, requires thread PK

### Views

`InboxView` - Display all message threads

`MessageCreateView` — Create a new message thread

`ThreadView` — View specific message thread

`ThreadDeleteView` — Delete specific message thread

### Forms

`NewMessageForm` — creates a new message thread to a single user

`NewMessageFormMultiple` — creates a new message thread to multiple users

`MessageReplyForm` - creates a reply to a message thread

### Templates

[Example templates](https://github.com/pinax/pinax-theme-bootstrap/tree/master/pinax_theme_bootstrap/templates/pinax/messages) are found in the `pinax-theme-bootstrap` [project](https://github.com/pinax/pinax-theme-bootstrap/tree/master/pinax_theme_bootstrap).

`pinax/messages/inbox.html` — Displays inbox message threads

`pinax/messages/thread_detail.html` — Show message thread and allow response

`pinax/messages/message_create.html` — New message form

### Signals

`message_sent` — `providing_args = ["message", "thread", "reply"]`

------

[Documentation Index](./index.md)

###