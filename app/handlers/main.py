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


tdir = os.path.join(os.path.dirname(__file__), '../templates/')


# OpenID Login
class LogIn(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        action = decode(self.request.get('action'))
        target_url = decode(self.request.get('continue'))
        if action and action == "verify":
            f = decode(self.request.get('openid_identifier'))
            url = users.create_login_url(target_url, federated_identity=f)
            self.redirect(url)
        else:
            self.response.out.write(template.render(tdir + "login.html", \
                    {"continue_to": target_url}))


class LogOut(webapp.RequestHandler):
    def get(self):
        url = users.create_logout_url("/")
        self.redirect(url)


# Custom sites
class Main(webapp.RequestHandler):
    def head(self, screen_name=None):
        """Head is used by Twitter, else the tweet button shows 0"""
        return

    def get(self):
        user = users.get_current_user()
        prefs = UserPrefs.from_user(user)

        param = decode(self.request.get('param'))

        self.response.out.write(template.render(tdir + "index.html", \
                {"prefs": prefs}))


class Account(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        prefs = UserPrefs.from_user(user)
        self.response.out.write(template.render(tdir + "index.html", \
                {"prefs": prefs}))
