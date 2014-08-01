import sys

from django.conf import settings


settings.configure(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
        }
    },
    ROOT_URLCONF="user_messages.urls",
    TEMPLATE_CONTEXT_PROCESSORS=[
        "user_messages.context_processors.user_messages",
    ],
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "user_messages",
    ]
)


from django_nose import NoseTestSuiteRunner

test_runner = NoseTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(["user_messages"])

if failures:
    sys.exit(failures)
