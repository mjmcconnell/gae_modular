"""Main application entry point.
"""

# third-party imports
import webapp2

# local imports
from modules.core import config
from modules.core import routes


app = webapp2.WSGIApplication(
    routes=routes.ROUTES,
    debug=config.DEBUG,
    config=config.CONFIG
)
