"""A collection of secure base handlers for webapp2-based applications.
"""
# stdlib imports
import functools

# third-party imports
from google.appengine.api import users


def requires_auth(f):
    """A decorator that requires a currently logged in user."""
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if not users.get_current_user():
            self.redirect('/')
        else:
            return f(self, *args, **kwargs)
    return wrapper


def requires_admin(f):
    """A decorator that requires a currently logged in administrator."""
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if not users.is_current_user_admin():
            self.redirect('/')
        else:
            return f(self, *args, **kwargs)
    return wrapper
