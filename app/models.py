# -*- coding: utf-8 -*-
import logging

from hashlib import md5

from google.appengine.ext import db
from google.appengine.api import users


class UserPrefs(db.Model):
    nickname = db.StringProperty()
    email = db.StringProperty(default="")
    email_md5 = db.StringProperty(default="")  # used for gravatar

    federated_identity = db.StringProperty()
    federated_provider = db.StringProperty()

    # google user id is only used on the dev server
    google_user_id = db.StringProperty()

    date_joined = db.DateTimeProperty(auto_now_add=True)
    date_lastlogin = db.DateTimeProperty(auto_now_add=True)  # TODO
    date_lastactivity = db.DateTimeProperty(auto_now_add=True)

    email = db.StringProperty(required=True)

    date_joined = db.DateTimeProperty(auto_now_add=True)
    date_lastlogin = db.DateTimeProperty(auto_now_add=True)

    boolean_property = db.BooleanProperty(default=True)

    @staticmethod
    def from_user(user):
        if not user:
            return None

        if not user.federated_identity():
            # Only happens on local devserver
            logging.warning("_ user has no fed id [%s]" % user)

        if user.federated_identity():
            q = db.GqlQuery("SELECT * FROM UserPrefs WHERE \
                federated_identity = :1 AND federated_provider = :2", \
                user.federated_identity(), user.federated_provider())
        else:
            # Only on the local devserver
            q = db.GqlQuery("SELECT * FROM UserPrefs WHERE \
                google_user_id = :1", user.user_id())

        prefs = q.get()
        if not prefs:
            # create regular new userpref object now
            nick = user.nickname()
            if user.email():
                if not nick or "http://" in nick:
                    # If user has email and openid-url is nickname, replace
                    nick = user.email()

            # Save the md5 for gravatar
            m = md5(user.email().strip().lower()).hexdigest()

            # Create new user preference entity
            logging.info("_ create new userprefs: %s" % nick)
            prefs = UserPrefs(nickname=nick, \
                    email=user.email(), \
                    email_md5=m, \
                    federated_identity=user.federated_identity(), \
                    federated_provider=user.federated_provider(), \
                    google_user_id=user.user_id()
                )

            # Save it
            prefs.put()

        # Return either found or newly created user preferences
        return prefs


class YourCustomModel(db.Model):
    userprefs = db.ReferenceProperty(UserPrefs)

    demo_string_property = db.StringProperty()
    demo_boolean_property = db.BooleanProperty(default=True)
    demo_integer_property = db.IntegerProperty(default=1)
    demo_datetime_property = db.DateTimeProperty(auto_now_add=True)
