#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import code, traceback, signal
import logging
from datetime import datetime

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
TIMEOUT = 15

def real_import(name):
    if '.'  in name:
        return reduce(getattr, name.split('.')[1:], __import__(name))
    return __import__(name)

logger = logging.getLogger('PyEsReduceRefineServiceApp')

def flush_dead_mappers(redis, mappers_key, ping_key):
    mappers = redis.smembers(mappers_key)
    for mapper in mappers:
        last_ping = redis.get(ping_key % mapper)
        if last_ping:
            now = datetime.now()
            last_ping = datetime.strptime(last_ping, DATETIME_FORMAT)
            if ((now - last_ping).seconds > TIMEOUT):
                logging.warning('MAPPER %s found to be inactive after %d seconds of not pinging back' % (mapper, TIMEOUT))
                redis.srem(mappers_key, mapper)
                redis.delete(ping_key % mapper)


def kls_import(fullname):
    if not '.' in fullname:
        return __import__(fullname)

    name_parts = fullname.split('.')
    klass_name = name_parts[-1]
    module_parts = name_parts[:-1]
    module = reduce(getattr, module_parts[1:], __import__('.'.join(module_parts)))
    klass = getattr(module, klass_name)
    return klass

def debug(sig, frame):
    """Interrupt running process, and provide a python prompt for
    interactive debugging."""
    d={'_frame':frame}         # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)

    i = code.InteractiveConsole(d)
    message  = "Signal recieved : entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    i.interact(message)

def listen():
    signal.signal(signal.SIGUSR1, debug)  # Register handler
