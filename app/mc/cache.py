# -*- coding: utf-8 -*-
import logging
from google.appengine.api import memcache

import models


def get_someitems(clear=False):
    """Boilerplate for your customization"""
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
    """
    Get the UserPrefs for the current user either from memcache or, if not
    yet cached, from the datastore and put it into memcache. Used by 
    UserPrefs.from_user(user)
    """
    if not user:
        return user

    if user.federated_identity():
        key = "userprefs_fid_%s" % user.federated_identity()
    else:
        key = "userprefs_gid_%s" % user.user_id()

    # Clearing the cache does not return anything
    if clear:
        memcache.delete(key)
        logging.info("- cache cleared key: %s", key)
        return

    # Try to grab the cached UserPrefs
    prefs = memcache.get(key)
    if prefs:
        logging.info("- returning cached userprefs for key: %s", key)
        return prefs

    # If not cached, query the datastore, put into cache and return object
    prefs = models.UserPrefs._from_user(user)
    memcache.set(key, prefs)
    logging.info("cached userprefs key: %s", key)
    return prefs
