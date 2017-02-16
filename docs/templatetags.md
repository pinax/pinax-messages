# Template Tags and Filters

## unread

Determines if a message thread has unread messages for a user.

**Argument**: `user`

For instance if there are unread messages in a thread, change the CSS class accordingly:

```html
{% load pinax_messages_tags %}

    <div class="thread {% if thread|unread:user %}unread{% endif %}">
    ...
    </div>
```

## unread_threads

Returns the number of unread threads for the user. Use for notifying a user of new messages, for example in _account_bar.html

**Argument**: `user`

For instance if there are unread messages in a thread, change the CSS class accordingly:

```html
{% load pinax_messages_tags %}

    <li class="{% if user|unread_threads %}unread{% endif %}">
        <a href="{% url 'pinax_messages:inbox' %}"><i class="fa fa-envelope"></i> {% trans "Messages" %}
            {% if user|unread_threads %}<sup>{{ user|unread_threads }}</sup>{% endif %}
        </a>
    </li>        
```

***
[Documentation Index](./index.md)
