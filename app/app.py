# -*- coding: utf-8 -*-
import os
from google.appengine.dist import use_library
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# Load database models
from models import *

# Load request handlers
from handlers import *

urls = [
    (r'/', Main),
    (r'/login', LogIn),
    (r'/_ah/login_required', LogIn),
    (r'/logout', LogOut),
    (r'/account', Account),
    (r'/account/setup', AccountSetup),
]

application = webapp.WSGIApplication(urls, debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
