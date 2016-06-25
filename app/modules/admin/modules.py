import collections


def fetch_routes():
    return AdminModules.fetch_routes()


class InvalidActionFoundException(Exception):
    pass


class AdminModule(object):
    """A class that holds module information."""

    ROUTES = []

    def __init__(self, name, label=None, routes=None):
        self._name = name
        self._label = label

        if routes:
            self.ROUTES = routes

    @property
    def enabled(self):
        return self._name in AdminModules.enabled

    @property
    def routes(self):
        """Module specific routes"""
        return self.ROUTES

    def load(self):
        """Preform setup steps for module"""
        if self._name not in AdminModules.enabled:
            AdminModules.enabled.add(self._name)


class AdminModules(object):
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
