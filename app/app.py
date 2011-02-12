from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# Load database models
from models import *

# Load request handlers
from handlers import *

urls = [
    (r'/', Main),
    #(r'/feeds', Feeds),
    #(r'/profile/([-\w]+)', Profile),
    #(r'/signin', SignIn),
    #(r'/signout', SignOut),
    #(r'/test', Test),
]

application = webapp.WSGIApplication(urls, debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
