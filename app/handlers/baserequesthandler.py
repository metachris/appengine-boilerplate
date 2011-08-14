# -*- coding: utf-8 -*-
import os
from google.appengine.api import users
from google.appengine.ext import webapp

import models
import tools.common
import settings

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),
        '../%s' % settings.TEMPLATE_DIR)


class BaseRequestHandler(webapp.RequestHandler):
    """Extension of the normal RequestHandler

    - self.userprefs provides the UserPrefs object of the current user.
    - self.render() provides a quick way to render templates with
      common template variables already preset.
    """
    def __init__(self):
        super(BaseRequestHandler, self).__init__()
        self.userprefs = models.UserPrefs.from_user(users.get_current_user())

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
        self.response.out.write(webapp.template.render(fn, values,
                debug=tools.common.is_testenv()))

    def head(self, *args):
        """Head is used by Twitter. If not there the tweet button shows 0"""
        pass
