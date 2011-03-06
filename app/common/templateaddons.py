# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from django.template import Node

"""
http://docs.djangoproject.com/en/dev/howto/custom-template-tags/

before rendering the template, include tags in the handler with
    webapp.template.register_template_library('common.templateaddons')
"""

# get registry, we need it to register our filter later.
register = webapp.template.create_template_register()


def getItem(l, id):
    """
    use template-tag with {{ my_tuple|getItem:0 }}
    workaround because appengine templates can't do {% for x,y in sometuple %}
    """
    if type(l) == list and len(l) > id:
        return l[id]
    if type(l) == dict and id in l:
        return l[id]


def truncate_chars(value, maxlen):
    if len(value) < maxlen:
        return value
    else:
        return value[:maxlen - 3] + '...'


register.filter(getItem)
register.filter(truncate_chars)
