"""`appengine_config` gets loaded when starting a new application instance.
"""
# stdlib imports
import sys
import os.path

# add `third_party` subdirectory to `sys.path`, so we can load third-party libraries.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'third_party'))
