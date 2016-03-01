#!/usr/bin/env python
import os
import sys

import django

from django.conf import settings


DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "django.contrib.sessions",
        "account",
        "pinax.messages",
        "pinax.messages.tests"
    ],
    MIDDLEWARE_CLASSES=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    ],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    SITE_ID=1,
    ROOT_URLCONF="pinax.messages.tests.urls",
    SECRET_KEY="notasecret",
    TEMPLATE_CONTEXT_PROCESSORS=[
        "user_messages.context_processors.user_messages",
    ],
    AUTHENTICATION_BACKENDS=[
        "account.auth_backends.UsernameAuthenticationBackend",
    ],
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
        },
    ]
)


def runtests(*test_args):
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    try:
        from django.test.runner import DiscoverRunner
        runner_class = DiscoverRunner
        test_args = ["pinax.messages.tests"]
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner
        runner_class = DjangoTestSuiteRunner
        test_args = ["tests"]

    failures = runner_class(verbosity=1, interactive=True, failfast=False).run_tests(test_args)
    sys.exit(failures)


if __name__ == "__main__":
    runtests(*sys.argv[1:])
