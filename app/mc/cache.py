# -*- coding: utf-8 -*-
from google.appengine.api import memcache
from models import *


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
    return pivots
