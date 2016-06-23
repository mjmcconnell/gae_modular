import collections


def fetch_routes():
    return AdminRegister.fetch_routes()


class AdminModule(object):
    """A class that holds module information."""

    def __init__(self, name, routes, on_load=None):
        self._name = name
        self._routes = routes

        AdminRegister.modules[self._name] = self

    def load(self):
        """Preform setup steps for module"""
        if self._name not in AdminRegister.enabled:
            AdminRegister.enabled.add(self._name)

    @property
    def enabled(self):
        return self._name in AdminRegister.enabled

    @property
    def routes(self):
        """Module specific routes"""
        if self._routes:
            return self._routes
        return []


class AdminRegister(object):
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
