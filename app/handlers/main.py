# -*- coding: utf-8 -*-
import os
import logging

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# Import packages from the project
import mc
from models import *
from tools import *

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '../templates/')


class BaseRequestHandler(webapp.RequestHandler):
    """Extension of the normal RequestHandler

    - self.userprefs provides the UserPrefs object of the current user.
    - self.generate() provides a quick way to render templates with
      common template variables already preset.
    """
    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.userprefs = UserPrefs.from_user(users.get_current_user())

    def render(self, template_name, template_values={}):
        # Preset values for the template
        values = {
          'request': self.request,
          'prefs': self.userprefs,
          'login_url': users.create_login_url(self.request.uri),
          'logout_url': users.create_logout_url(self.request.uri),
        }

        # Add manually supplied template values
        values.update(template_values)

        # Render template
        fn = os.path.join(TEMPLATE_DIR, template_name)
        self.response.out.write( \
                template.render(fn, values, debug=is_testenv()))

    def head(self, *args):
        """Head is used by Twitter, else the tweet button shows 0"""
        pass

    def get(self, *args):
        pass

    def post(self, *args):
        pass


# OpenID Login
class LogIn(webapp.RequestHandler):
    def get(self):
        action = decode(self.request.get('action'))
        target_url = decode(self.request.get('continue'))
        if action and action == "verify":
            fid = decode(self.request.get('openid_identifier'))
            url = users.create_login_url(target_url, federated_identity=fid)
            self.redirect(url)
        else:
            self.response.out.write( \
                    template.render(TEMPLATE_DIR + "login.html", 
                            {"continue_to": target_url}))


# LogOut redirects the user to the GAE logout url, and then redirects to /
class LogOut(webapp.RequestHandler):
    def get(self):
        url = users.create_logout_url("/")
        self.redirect(url)


# Main page request handler
class Main(BaseRequestHandler):
    def get(self):
        # UTF-8 decoding of a supplied parameter
        param = decode(self.request.get('param'))

        # Render the template
        self.render("index.html")


# Another page. Create a new html file for it!
class Account(BaseRequestHandler):
    def get(self):
        # Just render the template
        self.render("index.html")
