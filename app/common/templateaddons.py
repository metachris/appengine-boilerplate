# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from django.template import Node

"""
Custom template tags, for use from within the templates.

Before rendering a relevant template from within a handler, you need to include
the custom tags with this line of code:

    webapp.template.register_template_library('common.templateaddons')

More infos about custom template tags:

- http://docs.djangoproject.com/en/dev/howto/custom-template-tags/
"""

# get registry, we need it to register our filter later.
register = webapp.template.create_template_register()


def truncate_chars(value, maxlen):
    """Truncates value and appends '...' if longer than maxlen.
    Usage inside template to limit my_var to 20 characters max:

        {{ my_var|truncate_chars:20 }}

    """
    if len(value) < maxlen:
        return value
    else:
        return "%s..." % value[:maxlen - 3]


register.filter(truncate_chars)
