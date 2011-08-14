# -*- coding: utf-8 -*-
import os
import logging

from hashlib import md5
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
    - self.render() provides a quick way to render templates with
      common template variables already preset.
    """
    def __init__(self):
        super(BaseRequestHandler, self).__init__()
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
        """Head is used by Twitter. If not there the tweet button shows 0"""
        pass


# OpenID login
class LogIn(webapp.RequestHandler):
    """Redirects a user to the OpenID login site. Will redirect after 
    successful login if user is sent to /login?continue=/<target_url>.
    """
    def get(self):
        # Wrap target url in order to redirect new users to the account setup
        target_url = "/account?continue=%s" % decode(self.request.get('continue'))

        action = decode(self.request.get('action'))
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


# Account page and after-login handler
class Account(BaseRequestHandler):
    """After logging in, the user gets sent to /account?continue=<target_url>
    in order to finish setting up the account (email, username, newsletter). If
    the user account is already setup then simply redirect to the target url.

    Users not supplying ?continue=<url> will see the accounts.html page
    """
    def get(self):
        target_url = decode(self.request.get('continue'))        
        if target_url and "?continue=" in target_url:
            # circumvents a bug in gae which prepends the url again
            target_url = target_url[target_url.index("?continue=")+10:]

        if not self.userprefs.is_setup:
            # Setting up the user's preferences
            self.render("account_setup.html", {"target_url": target_url})
            return

        elif target_url:
            # If not a new user but ?continue=<url> supplied, redirect
            self.redirect(target_url)
            return

        # Render the account website
        self.render("account.html")


class AccountSetup(BaseRequestHandler):
    """Initial setup of the account, after user logs in the first time"""
    def post(self):
        username = decode(self.request.get("username"))
        email = decode(self.request.get("email"))
        subscribe = decode(self.request.get("subscribe"))
        target_url = decode(self.request.get('continue'))        
        if not target_url:
            target_url = "/account"

        self.userprefs.is_setup = True
        self.userprefs.nickname = username
        self.userprefs.email = email
        self.userprefs.email_md5 = md5(email.strip().lower()).hexdigest()
        self.userprefs.subscribed_to_newsletter = True if subscribe else False
        self.userprefs.put()

        logging.info("Updated UserPrefs")

        # Subscribe this user to the email newsletter now (if wanted)
        if subscribe:
            self.subscribe_to_newsletter()

        self.redirect(target_url)

    def subscribe_to_newsletter(self):
        # Use mailchimp api to add user to the list
        pass
