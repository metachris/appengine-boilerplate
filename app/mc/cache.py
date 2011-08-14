# -*- coding: utf-8 -*-
import logging

from google.appengine.api import memcache

import models


def get_someitems(clear=False):
    if clear:
        memcache.delete("someitems")
        return

    someitems = memcache.get("someitems")
    if someitems:
        #logging.info("return cached someitem")
        return someitems

    someitems = []
    for someitem in Someitem.all().fetch(100):
        someitems.append(someitem)

    memcache.set("someitems", someitems)
    logging.info("cached someitems")
    return someitems


def get_userprefs(user, clear=False):
    """Get the UserPrefs for the current user either from memcache or, if not
    yet cached, from the datastore and put it into memcache."""
    if not user:
        return user

    if user.federated_identity():
        key = "fid_%s" % user.federated_identity()
    else:
        key = "gid_%s" % user.user_id()

    # Clearing the cache. Does not return anything.
    if clear:
        memcache.delete("userprefs_%s" % key)
        logging.info("- cache cleared key: %s", key)
        return

    # If cached, return the cached UserPrefs now
    prefs = memcache.get("userprefs_%s" % key)
    if prefs:
        logging.info("- returning cached userprefs for key: %s", key)
        return prefs

    # If not cached, query the datastore, put into cache and return object
    prefs = models.UserPrefs._from_user(user)
    memcache.set("userprefs_%s" % key, prefs)
    logging.info("cached userprefs key: %s", key)
    return prefs
