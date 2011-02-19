from google.appengine.ext import webapp
from django.template import Node

# get registry, we need it to register our filter later.
register = webapp.template.create_template_register()


# template-tag: use with {{ somevar|half }}
# in the handler, before rendering the template, include tags with
#    webapp.template.register_template_library('common.templateaddons')
def half(n):
    if not type(n) in [int, long]:
        return n
    return n / 2

register.filter(half)
