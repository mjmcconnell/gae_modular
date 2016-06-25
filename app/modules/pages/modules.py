# stdlib imports
import collections

# local imports
from base.utils.routes import MultiPrefixRoute


def fetch_routes():
    return PageModules.fetch_routes()


class InvalidActionFoundException(Exception):
    pass


class AdminModule(object):
    """A class that holds module information."""

    ROUTES = []
    ALLOWED_API_ACTIONS = [
        'list',
        'read',
        'update',
        'delete',
    ]
    ALLOWED_TEMPLATE_ACTIONS = ['list', 'detail']

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

    def _set_api_routes(self, actions):
        routes = []
        for action in actions:
            if action not in self.ALLOWED_API_ACTIONS:
                raise InvalidActionFoundException(
                    'Invalid action api %s found', action)
            routes.append('{}ApiHandler'.fomat(action.capitalize()))

        self.ROUTES = self.ROUTES + MultiPrefixRoute(
            handler_pfx='modules.pages.handlers.apis.',
            name_pfx='api-pages-{}-'.format(self._name),
            path_pfx='/api/pages/{}'.format(self._name),
            routes=routes
        ).routes

    def _set_template_routes(self, actions):
        routes = []
        for action in actions:
            if action not in self.ALLOWED_TEMPLATE_ACTIONS:
                raise InvalidActionFoundException(
                    'Invalid action template %s found', action)
            routes.append('{}TemplateHandler'.fomat(action.capitalize()))

        self.ROUTES = self.ROUTES + MultiPrefixRoute(
            handler_pfx='modules.admin.handlers.templates.',
            name_pfx='admin-{}-template-'.format(self._name),
            path_pfx='/admin/{}'.format(self._name),
            routes=routes
        ).routes


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
