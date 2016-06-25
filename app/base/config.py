"""Application configuration"""
# stdlib imports
import os

# third-party imports
from google.appengine.api import app_identity

# local imports
from base.models import get_session_key

SERVER_SOFTWARE = os.environ.get('SERVER_SOFTWARE', 'Development')
DEBUG = SERVER_SOFTWARE.startswith('Development')


# Directory of the "core" module, used for global templates
BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
BASE_TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# fetch the app id for the serviing app
try:
    APP_ID = app_identity.get_application_id()
except AttributeError:
    APP_ID = 'testing'

if DEBUG:
    session_key = 'testingkey'
else:
    session_key = get_session_key()

# Root director of the app
ROOT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

CONFIG = {
    # Configure global context/filters/settings for Jinja2
    'jinja2': {
        'globals': {},
        'filters': {},
    },
    'webapp2_extras.sessions': {
        'secret_key': session_key,
    },
}

DEFAULT_MAIL_SENDER = 'mail@{}.appspotmail.com'.format(APP_ID)
