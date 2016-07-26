import codecs

from os import path
from setuptools import find_packages, setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


setup(
    author="Pinax Developers",
    author_email="developers@pinaxproject.com",
    description="a reusable private user messages application for Django",
    name="pinax-messages",
    long_description=read("README.rst"),
    version="0.3",
    url="http://github.com/pinax/pinax-messages/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "messages": []
    },
    test_suite="runtests.runtests",
    tests_require=[
        "django-test-plus>=1.0.11",
        "pinax-theme-bootstrap>=7.4.0",
    ],
    install_requires=[
        "django-appconf>=1.0.1",
        "django-user-accounts>=1.3.1"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
