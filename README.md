![](http://pinaxproject.com/pinax-design/patches/pinax-messages.svg)

# Pinax Messages

[![](https://img.shields.io/pypi/v/pinax-messages.svg)](https://pypi.python.org/pypi/pinax-messages/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-messages.svg)](https://circleci.com/gh/pinax/pinax-messages)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-messages.svg)](https://codecov.io/gh/pinax/pinax-messages)
[![](https://img.shields.io/github/contributors/pinax/pinax-messages.svg)](https://github.com/pinax/pinax-messages/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-messages.svg)](https://github.com/pinax/pinax-messages/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-messages.svg)](https://github.com/pinax/pinax-messages/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://pypi.python.org/pypi/pinax-messages/)


## Table of Contents

* [About Pinax](#about-pinax)
* [Important Links](#important-links)
* [Overview](#overview)
  * [Supported Django and Python Versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Template Tags and Filters](#template-tags-and-filters)
  * [Reference Guide](#reference-guide)
    * [Views](#views)
    * [Forms](#forms)
    * [Templates](#templates)
    * [Signals](#signals)
* [Change Log](#change-log)
* [History](#history)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.


## Important Links

Where you can find what you need:
* Releases: published to [PyPI](https://pypi.org/search/?q=pinax) or tagged in app repos in the [Pinax GitHub organization](https://github.com/pinax/)
* Global documentation: [Pinax documentation website](https://pinaxproject.com/pinax/)
* App specific documentation: app repos in the [Pinax GitHub organization](https://github.com/pinax/)
* Support information: [SUPPORT.md](https://github.com/pinax/.github/blob/master/SUPPORT.md) file in the [Pinax default community health file repo](https://github.com/pinax/.github/)
* Contributing information: [CONTRIBUTING.md](https://github.com/pinax/.github/blob/master/CONTRIBUTING.md) file in the [Pinax default community health file repo](https://github.com/pinax/.github/)
* Current and historical release docs: [Pinax Wiki](https://github.com/pinax/pinax/wiki/)


## pinax-messages

### Overview

`pinax-messages` is an app for providing private user-to-user threaded messaging.

#### Supported Django and Python Versions

Django / Python | 3.6 | 3.7 | 3.8
--------------- | --- | --- | ---
2.2  |  *  |  *  |  *
3.0  |  *  |  *  |  *


## Documentation

### Installation

To install pinax-messages:

```shell
    $ pip install pinax-messages
```

Add `pinax.messages` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    # other apps
    "pinax.messages",
]
```

Run Django migrations to create `pinax-messages` database tables:

```shell
    $ python manage.py migrate
```

Add `pinax.messages.urls` to your project urlpatterns:

```python
    urlpatterns = [
        # other urls
        url(r"^messages/", include("pinax.messages.urls", namespace="pinax_messages")),
    ]
```

### Usage

`pinax-messages` handles user-to-user private threaded messaging primarily by the inclusion of template snippets.
These snippets fall into three categories: view message inbox (all threads), view message thread, and create (or respond to) a message.

#### Access Inbox

Place this snippet wherever a "Message Inbox" link is needed for viewing user message inbox:

```django
<a href="{% url 'pinax_messages:inbox' %}"><i class="fa fa-envelope"></i> {% trans "Message Inbox" %}</a>
```

#### View Message Thread

Place this snippet wherever you have need to view a specific message thread:

```django
<a href="{% url 'pinax_messages:thread_detail' thread.pk %}"><i class="fa fa-envelope"></i> {% trans "View Message Thread" %}</a>
```

#### Create Message - Template

Add the following line to an object template in order to provide a button for messaging a user associated with `object`:

```django
<a href="{% url "pinax_messages:message_user_create" user_id=object.user.id %}" class="btn btn-default">Message this user</a>
```

#### Create Message - Code

Use the following code to create a new message programmatically. Note that `to_users` (message recipients) is a list, allowing messages sent to multiple users.

```python
from pinax.messages.models import Message

Message.new_message(from_user=self.request.user, to_users=[user], subject=subject, content=content)
```

#### Template Context Variables

`pinax-messages` provides two context variables using a template context processor. In order to access these in your templates, add `user_messages` to your `TEMPLATES` settings:

```python
TEMPLATES = [
    {
        # ...
        "OPTIONS": {
            # other options
            "context_processors": [
                # other processors
                "pinax.messages.context_processors.user_messages"
            ],
        },
    },
]
```

The following context variables are available, and work with the current authenticated user:

* `inbox_threads` — all message threads for current user
* `unread_threads` — unread message threads for current user

### Template Tags and Filters

#### unread

Determines if a message thread has unread messages for a user.

**Argument**: `user`

For instance if there are unread messages in a thread, change the CSS class accordingly:

```django
{% load pinax_messages_tags %}

    <div class="thread {% if thread|unread:user %}unread{% endif %}">
    ...
    </div>
```

#### unread_thread_count

Returns the number of unread threads for the user. Use for notifying a user of new messages, for example in _account_bar.html_

**Argument**: `user`

For instance if there are unread messages in a thread, change the CSS class accordingly:

```django
{% load pinax_messages_tags %}

    {% with user|unread_thread_count as user_unread %}
    <li class="{% if user_unread %}unread{% endif %}">
        <a href="{% url 'pinax_messages:inbox' %}"><i class="fa fa-envelope"></i> {% trans "Messages" %}
            {% if user_unread %}<sup>{{ user_unread }}</sup>{% endif %}
        </a>
    </li>        
    {% endwith %}
```

### Reference Guide

#### URL–View–Template Matrix

| URL Name                             | View                  | Template              |
| ------------------------------------ | --------------------- | --------------------- |
| `pinax-messages:inbox`               | `InboxView()`         | `inbox.html`          |
| `pinax-messages:message_create`      | `MessageCreateView()` | `message_create.html` |
| `pinax-messages:message_user_create` | `MessageCreateView()` | `message_create.html` |
| `pinax-messages:thread_detail`       | `ThreadView()`        | `thread_detail.html`  |
| `pinax-messages:thread_delete`       | `ThreadDeleteView()`  | N/A                   |

#### URL Names

These URL names are available when using pinax-messages urls.py:

`pinax-messages:inbox` — Inbox view

`pinax-messages:message_create` — Create new message

`pinax-messages:message_user_create` — Create new message to specific user

`pinax-messages:thread_detail` — View message thread, requires thread PK

`pinax-messages:thread_delete` — Delete message thread, requires thread PK

#### Views

`InboxView` - Display all message threads

`MessageCreateView` — Create a new message thread

`ThreadView` — View specific message thread

`ThreadDeleteView` — Delete specific message thread

#### Forms

`NewMessageForm` — creates a new message thread to a single user

`NewMessageFormMultiple` — creates a new message thread to multiple users

`MessageReplyForm` - creates a reply to a message thread

#### Templates

Default templates are provided by the `pinax-templates` app in the
[messages](https://github.com/pinax/pinax-templates/tree/master/pinax/templates/templates/pinax/messages)
section of that project.

Reference pinax-templates
[installation instructions](https://github.com/pinax/pinax-templates/blob/master/README.md#installation)
to include these templates in your project.

View live `pinax-templates` examples and source at [Pinax Templates](https://templates.pinaxproject.com/messages/inbox-empty/)!

##### Customizing Templates

Override the default `pinax-templates` templates by copying them into your project
subdirectory `pinax/messages/` on the template path and modifying as needed.

For example if your project doesn't use Bootstrap, copy the desired templates
then remove Bootstrap and Font Awesome class names from your copies.
Remove class references like `class="btn btn-success"` and `class="icon icon-pencil"` as well as
`bootstrap` from the `{% load i18n bootstrap %}` statement.
Since `bootstrap` template tags and filters are no longer loaded, you'll also need to update
`{{ form|bootstrap }}` to `{{ form }}` since the "bootstrap" filter is no longer available.

##### `inbox.html`

Displays inbox message threads.

##### `thread_detail.html`

Show message thread and allow response.

##### `message_create.html`

New message form.

#### Signals

`message_sent` — `providing_args = ["message", "thread", "reply"]`


## Change Log

### 3.0.0

* Drop Django 1.11, 2.0, and 2.1, and Python 2,7, 3.4, and 3.5 support
* Add Django 2.2 and 3.0, and Python 3.6, 3.7, and 3.8 support
* Update packaging configs
* Direct users to community resources

### 2.0.2

* Update CI config
* Update MANIFEST.in
* Add sorting guidance for 3rd-party app imports
* Improve documentation markup
* Remove pinax-theme-bootstrap from test requirements

### 2.0.1

* Update test config
* Update documentation

### 2.0.0

* Standardize documentation layout
* Drop Django v1.8, v1.10 support

### 1.2.0

* Add `unread_thread_count` template filter

### 1.1.0

* Add Django 2.0 compatibility testing
* Drop Django 1.9 and Python 3.3 support
* Move documentation into README
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description

### 1.0.1

- Fix thread delete view with correct template path and success URL

### 1.0.0

- add documentation

### 0.3

- convert to Django generic CBVs
- various fixes and cleanup

### 0.1

- initial release


## History

This app was formerly named `user-messages` but was renamed after being donated to Pinax from Eldarion.


## Contribute

[Contributing](https://github.com/pinax/.github/blob/master/CONTRIBUTING.md) information can be found in the [Pinax community health file repo](https://github.com/pinax/.github).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a [Code of Conduct](https://github.com/pinax/.github/blob/master/CODE_OF_CONDUCT.md). We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject) and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-present James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).
