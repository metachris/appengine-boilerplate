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


# Google sites
class LogIn(webapp.RequestHandler):
    def get(self):
        html = env.get_template('login.html').render()
        self.response.out.write(html)
        #user = users.get_current_user()
        #url = users.create_login_url("/")
        #self.redirect(url)


class LogOut(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url("/")
        self.redirect(url)


# Custom sites
class Main(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        html = env.get_template('index.html').render({'user': user})
        self.response.out.write(html)
