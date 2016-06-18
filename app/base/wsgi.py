"""Main application entry point.
"""
# stdlib imports
import os

# third-party imports
import webapp2

# local imports
from base import config


def _get_routes():
    """Routes for all enabled modules
    """
    routes = []
    modules = os.environ.get('ENABLED_MODULES', '').split()
    for module in modules:
        mod_path = '.'.join(['modules', module])
        mod_routes_path = '.'.join([mod_path, 'routes'])
        mod_routes = __import__(mod_routes_path, fromlist=[''])
        # Extend the routes list with the modules routes
        routes = routes + mod_routes.ROUTES

    return routes


app = webapp2.WSGIApplication(
    routes=_get_routes(),
    debug=config.DEBUG,
    config=config.CONFIG
)
