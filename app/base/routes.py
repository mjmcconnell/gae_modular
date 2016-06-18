"""Route/URL definitions for all modules"""
# stdlib imports
import os
import re
import importlib

# local imports
from base.config import ROOT_DIR


def _get_routes():
    """Routes for all modules
    """
    routes = []
    modules_path = os.path.join(ROOT_DIR, 'modules')
    # Ensure the modules dir is
    if os.path.isdir(modules_path):
        # Loop through all the modules
        for module in os.listdir(modules_path):
            # If a module has a 'routes.py' file exists, then import routes,
            # via the "ROUTES" variable in the routes.py file
            full_module_path = os.path.join(modules_path, module, 'routes.py')
            if os.path.exists(full_module_path):
                # Strip off the root path to make it relative to the app
                rel_path = full_module_path[:].replace(ROOT_DIR, '')
                # Replace directory separators with peroids
                py_path = re.sub('[\\/]', '.', rel_path)
                # Import the routes module
                module_routes = __import__(py_path[1:-3], fromlist=[''])
                # Extend the routes list with the modules routes
                routes = routes + module_routes.ROUTES

    return routes


ROUTES = _get_routes()
