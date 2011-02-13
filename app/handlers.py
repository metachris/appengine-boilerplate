import os

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from models import *

# Setup jinja templating
template_dirs = []
template_dirs.append(os.path.join(os.path.dirname(__file__), 'templates'))
env = Environment(loader=FileSystemLoader(template_dirs))


# OpenID Login
class LogIn(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        action = self.request.get('action')
        target_url = self.request.get('continue')
        if action and action == "verify":
            f = self.request.get('openid_identifier')
            url = users.create_login_url(target_url, federated_identity=f)
            self.redirect(url)
        else:
            html = env.get_template('login.html').render()
            self.response.out.write(html)


class LogOut(webapp.RequestHandler):
    def get(self):
        url = users.create_logout_url("/")
        self.redirect(url)


# Custom sites
class Main(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        html = env.get_template('index.html').render({'user': user})
        self.response.out.write(html)


class Account(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        html = env.get_template('index.html').render({'user': user})
        self.response.out.write(html)
