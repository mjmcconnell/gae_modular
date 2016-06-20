"""`appengine_config` gets loaded when starting a new application instance.
"""
# stdlib imports
import sys
import os.path

# add `third_party` subdirectory to `sys.path`, so we can load third-party libraries.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'third_party'))


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


_enable_modules()
