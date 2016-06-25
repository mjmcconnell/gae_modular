"""Main application entry point.
"""
# third-party imports
import webapp2

# local imports
from base import config
from base import modules

app = webapp2.WSGIApplication(
    routes=modules.fetch_routes(),
    debug=config.DEBUG,
    config=config.CONFIG
)
