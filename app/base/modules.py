class Module(object):
    """A class that holds module information."""

    def __init__(self, routes, on_load=None):
        self._routes = routes
        self._on_load = on_load

    def load(self):
        """Preform setup steps for module"""
        if self._on_load:
            self._on_load()

    def routes(self):
        """Module specific routes"""
        if self._routes:
            return self._routes
        return []
