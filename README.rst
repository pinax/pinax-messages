Pinax Messages
==============

.. image:: http://slack.pinaxproject.com/badge.svg
   :target: http://slack.pinaxproject.com/

.. image:: https://img.shields.io/travis/pinax/pinax-messages.svg
   :target: https://travis-ci.org/pinax/pinax-messages

.. image:: https://img.shields.io/coveralls/pinax/pinax-messages.svg
   :target: https://coveralls.io/r/pinax/pinax-messages

.. image:: https://img.shields.io/pypi/dm/pinax-messages.svg
   :target:  https://pypi.python.org/pypi/pinax-messages/

.. image:: https://img.shields.io/pypi/v/pinax-messages.svg
   :target:  https://pypi.python.org/pypi/pinax-messages/

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target:  https://pypi.python.org/pypi/pinax-messages/

Pinax
-----

Pinax is an open-source platform built on the Django Web Framework. It is an
ecosystem of reusable Django apps, themes, and starter project templates.
This collection can be found at http://pinaxproject.com.

pinax-messages
---------------

``pinax-messages`` is an application for allowing users of your Django site to
send messages to each other.

This app was formerly named ``user-messages`` but was renamed after being donated to
Pinax from Eldarion.



Getting Started
----------------

Include ``pinax-messages`` in your requirements file and add
``"pinax.messages"`` to your INSTALLED APPS setting.

Once you have the ``pinax-messages`` installed, hook up the URLs::

    urlpatterns = patterns("",
        # some cool URLs

        (r"^messages/", include("pinax.messages.urls")),

        # some other cool URLs
    )

Now all you need to do is wire up some templates.


Running the Tests
-------------------

    ::

       $ pip install detox
       $ detox


Documentation
---------------
The ``pinax-messages`` documentation is currently under construction. If you would like to help us write documentation, please join our Slack team and let us know!
The Pinax documentation is available at http://pinaxproject.com/pinax/.


Contribute
----------------

See this blog post http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/ including a video, or our How to Contribute (http://pinaxproject.com/pinax/how_to_contribute/) section for an overview on how contributing to Pinax works. For concrete contribution ideas, please see our Ways to Contribute/What We Need Help With (http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions, we recommend you join our Pinax Slack team (http://slack.pinaxproject.com) and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course also valid but we are usually able to help you faster if you ping us in Slack.

We also highly recommend reading our Open Source and Self-Care blog pos ](http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/).  


Code of Conduct
----------------

In order to foster a kind, inclusive, and harassment-free community, the Pinax
Project has a code of conduct, which can be found here
http://pinaxproject.com/pinax/code_of_conduct/. We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


Pinax Project Blog and Twitter
--------------------------------

For updates and news regarding the Pinax Project, please follow us on Twitter at
@pinaxproject and check out our blog http://blog.pinaxproject.com.
