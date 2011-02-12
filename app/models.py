from google.appengine.ext import db
from google.appengine.api import users


class UserPrefs(db.Model):
    user = db.UserProperty(required=True)
    email = db.StringProperty(required=True)

    date_joined = db.DateTimeProperty(auto_now_add=True)
    date_lastlogin = db.DateTimeProperty(auto_now_add=True)

    boolean_property = db.BooleanProperty(default=True)


def getUserPrefs(user):
    """Get or create user preference object"""
    if user:
        q = db.GqlQuery("SELECT * FROM UserPrefs WHERE user = :1", user)
        prefs = q.get()
        if not prefs:
            prefs = UserPrefs(user=user, email=user.email())
            prefs.put()
        return prefs
