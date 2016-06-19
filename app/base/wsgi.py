"""Main application entry point.
"""
# stdlib imports
import os

# third-party imports
import webapp2

# local imports
from base import config


ROUTES = []


def _enable_modules():
    """Routes for all enabled modules
    """
    modules = os.environ.get('ENABLED_MODULES', '').split()
    for module_path in modules:
        _module = __import__(module_path, fromlist=[''])
        # Extend the routes list with the modules routes
        Module = _module.register_module()
        # Perform module setup steps
        Module.load()
        # Register the modules routes
        global ROUTES
        ROUTES = ROUTES + Module.routes


_enable_modules()


app = webapp2.WSGIApplication(
    routes=ROUTES,
    debug=config.DEBUG,
    config=config.CONFIG
)
