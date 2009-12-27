#!/usr/bin/env python
# encoding: utf-8

import collections
import weakref
from _weakrefset import WeakSet
from twisted.internet import reactor
import pyhkal.davenport
import pyhkal.shopping

listeners = collections.defaultdict(WeakSet)
#+ support subcommands
commands = weakref.WeakValueDictionary()
# dict of str -> (callback, dict of str -> (callback, dict ...))

def run(location=None):
    """Run PyHKAL on a CouchDB available at `location`."""
    davenport = pyhkal.davenport.Davenport(location)
    for mod in davenport.remember("modules"):
        pyhkal.shopping.buy(mod)
    dispatch_event("startup")
    reactor.run()

def add_listener(event, listener):
    listeners[event].add(listener)

def dispatch_event(event, *args):
    for dispatcher in listeners[event]:
        dispatcher(*args)

def add_command(command, listener, parent=None):
    #+ support subcommands
    if command in commands:
        raise SystemError
    commands[command] = listener

def dispatch_command(origin, command, args):
    #+ subcommand dispatch
    #+ check for number of arguments
    if command in commands:
        commands[command](origin, args)

class Origin(object):
    def __init__(self, typ, user, public=None):
        self.type = typ # of (query, channel, notice, dcc, web)
        self.user = user
        self.public = public
# origin:
#   query (user)
#   notice (user, channel)
#   channel (user, channel)
#   dcc (user)
#   web (user)
