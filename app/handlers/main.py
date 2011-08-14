# -*- coding: utf-8 -*-
import os
import logging

from hashlib import md5
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# Import packages from the project
import mc
import settings
import tools.mailchimp

from models import *
from baserequesthandler import BaseRequestHandler
from tools.common import decode
from tools.decorators import login_required


# OpenID login
class LogIn(BaseRequestHandler):
    """
    Redirects a user to the OpenID login site. After successful login the user
    redirected to the target_url (via /login?continue=/<target_url>).
    """
    def get(self):
        # Wrap target url to redirect new users to the account setup step
        target_url = "/account?continue=%s" % \
                decode(self.request.get('continue'))

        action = decode(self.request.get('action'))
        if action and action == "verify":
            fid = decode(self.request.get('openid_identifier'))
            url = users.create_login_url(target_url, federated_identity=fid)
            self.redirect(url)
        else:
            # BaseRequestHandler provides .render() for rendering a template
            self.render("login.html", {"continue_to": target_url})


# LogOut redirects the user to the GAE logout url, and then redirects to /
class LogOut(webapp.RequestHandler):
    def get(self):
        url = users.create_logout_url("/")
        self.redirect(url)


# Main page request handler
class Main(BaseRequestHandler):
    def get(self):
        # Render the template
        self.render("index.html")


# Account page and after-login handler
class Account(BaseRequestHandler):
    """
    The user's account and preferences. After the first login, the user is sent
    to /account?continue=<target_url> in order to finish setting up the account
    (email, username, newsletter).
    """
    def get(self):
        target_url = decode(self.request.get('continue'))
        # Circumvent a bug in gae which prepends the url again
        if target_url and "?continue=" in target_url:
            target_url = target_url[target_url.index("?continue=") + 10:]

        if not self.userprefs.is_setup:
            # First log in of user. Finish setup before forwarding.
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
        target_url = target_url or "/account"

        # Set a flag whether newsletter subscription setting has changed
        subscription_changed = bool(self.userprefs.subscribed_to_newsletter) \
                is not bool(subscribe)

        # Update UserPrefs object
        self.userprefs.is_setup = True
        self.userprefs.nickname = username
        self.userprefs.email = email
        self.userprefs.email_md5 = md5(email.strip().lower()).hexdigest()
        self.userprefs.subscribed_to_newsletter = bool(subscribe)
        self.userprefs.put()

        # Subscribe this user to the email newsletter now (if wanted). By
        # default does not subscribe users to mailchimp in Test Environment!
        if subscription_changed and settings.MAILCHIMP_ENABLED:
            if subscribe:
                tools.mailchimp.mailchimp_subscribe(email)
            else:
                tools.mailchimp.mailchimp_unsubscribe(email)

        # After updating UserPrefs, redirect
        self.redirect(target_url)
