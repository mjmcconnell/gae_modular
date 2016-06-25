# future imports
from __future__ import absolute_import

# stdlib imports
import collections


def fetch_routes():
    return PageModules.fetch_routes()


class PageModule(object):
    """A class that holds module information."""

    ROUTES = []

    def __init__(self, name, label):
        self._name = name
        self._label = label

    @property
    def enabled(self):
        return self._name in PageModules.enabled

    @property
    def routes(self):
        """Module specific routes"""
        return self.ROUTES

    def load(self):
        """Preform setup steps for module"""
        if self._name not in PageModules.enabled:
            PageModules.enabled.add(self._name)


class PageModules(object):
    """A registry that holds all custom modules."""

    modules = collections.OrderedDict()
    enabled = set()

    @classmethod
    def fetch_routes(cls):
        routes = []
        for module in cls.modules.values():
            if module.enabled:
                routes += module.routes
        return routes
