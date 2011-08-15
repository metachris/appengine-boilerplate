# -*- coding: utf-8 -*-
import logging

from hashlib import md5
from google.appengine.ext import db
from google.appengine.api import users

import mc


class UserPrefs(db.Model):
    """Storage for custom properties related to a user. Provides caching
    for super-fast access to the UserPrefs object.

    All models with user relations should reference the specific UserPrefs
    model, never the GAE internal user model (due to a known GAE bug).

    The UserPrefs can be retrieved/created via from_user(user):

        userprefs = UserPrefs.from_user(users.get_current_user())

    This retrieves the UserPrefs object is automatically from memcache or, if
    not already cached, from the datastore and put into memcache. The cached
    object is cleared whenever the .put() or .delete() method is called.

    If users.get_current_user() is not logged in, from_user() returns None.

    The BaseRequestHandler (see handlers/baserequesthandler.py and main.py)
    automatically provides the current UserPref object via self.userprefs.
    """
    # Base settings. Copied over from OpenID at first login (may not be valid)
    nickname = db.StringProperty()
    email = db.StringProperty(default="")

    # The md5 has of the email is used for gravatar image urls
    email_md5 = db.StringProperty(default="")

    # email_verified is set after user clicked the link in verification mail
    email_verified = db.BooleanProperty(default=False)

    # The main reference to the Google-internal user object
    federated_identity = db.StringProperty()
    federated_provider = db.StringProperty()

    # Google user id is only used on the dev server
    google_user_id = db.StringProperty()

    # Various meta information
    date_joined = db.DateTimeProperty(auto_now_add=True)
    date_lastlogin = db.DateTimeProperty(auto_now_add=True)  # TODO
    date_lastactivity = db.DateTimeProperty(auto_now_add=True)  # TODO

    # is_setup: set to true after setting username and email at first login
    is_setup = db.BooleanProperty(default=False)

    # Cursom properties
    subscribed_to_newsletter = db.BooleanProperty(default=False)

    @staticmethod
    def from_user(user):
        """Returns the cached UserPrefs object. If not cached, get from DB and
        put it into memcache."""
        if not user:
            return None

        return mc.cache.get_userprefs(user)

    @staticmethod
    def _from_user(user):
        """Gets UserPrefs object from database. Used by
        mc.cache.get_userprefs() if not cached."""
        if user.federated_identity():
            # Standard OpenID user object
            q = db.GqlQuery("SELECT * FROM UserPrefs WHERE \
                federated_identity = :1", user.federated_identity())

        else:
            # On local devserver there is only the google user object
            q = db.GqlQuery("SELECT * FROM UserPrefs WHERE \
                google_user_id = :1", user.user_id())

        # Try to get the UserPrefs from the data store
        prefs = q.get()

        # If not existing, create now
        if not prefs:
            nick = user.nickname()
            if user.email():
                if not nick or "http://" in nick or "https://" in nick:
                    # If user has email and openid-url is nickname, replace
                    nick = user.email()

            # Create new user preference entity
            logging.info("Creating new UserPrefs for %s" % nick)
            prefs = UserPrefs(nickname=nick,
                    email=user.email(),
                    email_md5=md5(user.email().strip().lower()).hexdigest(),
                    federated_identity=user.federated_identity(),
                    federated_provider=user.federated_provider(),
                    google_user_id=user.user_id())

            # Save the newly created UserPrefs
            prefs.put()

        # Keep an internal reference to the Google user object (for
        # clearing the cache).
        prefs._user = user

        # Return either found or just created user preferences
        return prefs

    def put(self):
        """
        Overrides db.Model.put() to remove the cached object after an update.
        """
        # Call the put() method of the db.Model and keep the result
        key = super(UserPrefs, self).put()

        # Remove previously cached object. If put() is called the first time
        # (after creating the object) there would be no self._user.
        if hasattr(self, "_user"):
            self._clear_cache()

        # Return key provided by db.Model.put()
        return key

    def delete(self):
        """
        Overrides db.Model.delete() to remove the object from memcache.
        """
        super(UserPrefs, self).delete()
        self._clear_cache()

    def _clear_cache(self):
        """
        Removes the object from memcache. Automatically called on .put()
        and .delete().
        """
        mc.cache.get_userprefs(self._user, clear=True)


class YourCustomModel(db.Model):
    userprefs = db.ReferenceProperty(UserPrefs)

    demo_string_property = db.StringProperty()
    demo_boolean_property = db.BooleanProperty(default=True)
    demo_integer_property = db.IntegerProperty(default=1)
    demo_datetime_property = db.DateTimeProperty(auto_now_add=True)
