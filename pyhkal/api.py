# encoding: utf-8

import inspect
from distutils.version import LooseVersion
import pyhkal.engine
import pyhkal.fred
import pyhkal.shopping

class Api(object):
    def __init__(self, davenport):
        self.davenport = davenport
    def hi(self, **meta):
        """
        >>> hi(
        ...     version = "1.0",
        ...     depends = [
        ...         "modname",
        ...     ],
        ... )

        """
        frame = inspect.currentframe().f_back
        mod = frame.f_globals
        if 'depends' in meta:
            for dependency in meta['depends']:
                dep = LooseVersion(dependency).version[0]
                mod[dep] = pyhkal.shopping.buy(dep)
        mod['__metadata__'] = meta

    def hook(self, event, *args):
        def deco(func):
            pyhkal.engine.add_listener(event, func)
            return func
        return deco

    def register(self, func):
        name = func.__name__
        pyhkal.engine.add_command(name, func)
        return func

    def send(self, message, dest=None):
        dispatch_event('send', message)

    dispatch_command = staticmethod(pyhkal.engine.dispatch_command)
    thread = staticmethod(pyhkal.fred.threaded)
