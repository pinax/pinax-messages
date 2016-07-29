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

***
[Documentation Index](./index.md)
