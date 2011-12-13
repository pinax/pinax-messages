from distutils.core import setup


setup(
    name = "user-messages",
    version = "0.1",
    author = "Eldarion",
    author_email = "development@eldarion.com",
    description = "a reusable private user messages application for Django",
    long_description = open("README.rst").read(),
    license = "BSD",
    url = "http://github.com/eldarion/user_messages",
    packages = [
        "user_messages",
        "user_messages.tests",
        "user_messages.templatetags",
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
