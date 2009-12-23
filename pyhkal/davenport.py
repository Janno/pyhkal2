#!/usr/bin/env python

"""
Document storage.

One davenport oughta be enough for anybody. (This module is a singleton.)

The davenport described herein is both, a sofa and a desk.
"""

DATABASE = 'pyhkal'
REMEMBER = 'config'

import couchdb.client

class Davenport(object):
    def __init__(self, location=None):
        """Create a davenport storing your documents. `location` can be used to
        occupy a remote davenport. Otherwise use your local desk.

        """
        server = couchdb.client.Server(location or couchdb.client.DEFAULT_BASE_URI)
        try:
            self._sofa = server[DATABASE]
        except couchdb.client.ResourceNotFound:
            self._sofa = server.create(DATABASE)

    def get_by_label(self, label):
        return self._sofa[label]

    _none = object()
    def remember(self, breadcrumbs, default=_none):
        """Remember that random fact that popped into your head 2 AM in the
        morning. For some weird reason, you need a sofa to remember.

        """
        config = self.get_by_label(REMEMBER)
        try:
            return reduce(lambda doc, value: doc[value],
                    breadcrumbs.split(), config)
        except KeyError:
            if default is not self._none:
                return default
            raise
