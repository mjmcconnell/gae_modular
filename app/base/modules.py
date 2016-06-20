import collections
import logging


def fetch_routes():
    return RegisteredModules.fetch_routes()


class Module(object):
    """A class that holds module information."""

    def __init__(self, name, routes, on_load=None):
        self._name = name
        self._routes = routes
        self._on_load = on_load

        RegisteredModules.modules[self._name] = self

    def load(self):
        """Preform setup steps for module"""
        if self._name not in RegisteredModules.enabled:
            logging.info('Enabling module: %s', self._name.upper())
            RegisteredModules.enabled.add(self._name)
            if self._on_load:
                self._on_load()

    @property
    def enabled(self):
        return self._name in RegisteredModules.enabled

    @property
    def routes(self):
        """Module specific routes"""
        if self._routes:
            return self._routes
        return []


class RegisteredModules(object):
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
