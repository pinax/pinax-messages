## Installation

### Install `pinax-messages`

* Add `"pinax-messages"` to your `requirements.txt` file or install pinax-messages manually:

```
$ pip install pinax-messages
```

* Add `"pinax.messages"` to your `INSTALLED_APPS` setting:

```python
    INSTALLED_APPS = (
        ...
        "pinax.messages"
        ...
    )
```

### Run Migrations

* Run Django migrations to create `pinax-messages` database tables:

```
$ python manage.py migrate
```

### Hook Up URLs

Add `pinax.messages.urls` to your project urlpatterns:

```python
    urlpatterns = [
        ...
        url(r"^messages/", include("pinax.messages.urls", namespace="pinax_messages")),
        ...
    ]
```

See [Usage](./usage.md) for details about integrating pinax-messages with your project.
See [Template Tags and Filters](./templatetags.md) for details about included tags and filters.
See [Reference Guide](./reference.md) for details about URL and template names.

***
[Documentation Index](./index.md)