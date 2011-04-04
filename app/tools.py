# -*- coding: utf-8 -*-
import re
import logging
from os import environ

_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')


def is_testenv():
    """
    True if devserver, False if appengine server

    Appengine uses  'Google App Engine/1.4.2',
    Devserver  uses 'Development/1.0'
    """
    return environ.get('SERVER_SOFTWARE', '').startswith('Development')


def decode(var):
    """Decode form input"""
    if not var:
        return var
    return unicode(var, 'utf-8') if isinstance(var, str) else unicode(var)


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-ascii characters,
    and converts spaces to hyphens.

    From Django's "django/template/defaultfilters.py".
    """
    if not isinstance(value, unicode):
        value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(_slugify_strip_re.sub('', value).strip().lower())
    return _slugify_hyphenate_re.sub('-', value)
