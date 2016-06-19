"""Base handlers for modules
"""
# future imports
from __future__ import absolute_import

# stdlib imports
import webapp2

# third-party imports
from google.appengine.api import users
from webapp2_extras import sessions


class SecurityError(Exception):
    """Exception wrapper for security specific exceptions
    """
    pass


class BaseHandler(webapp2.RequestHandler):
    """Base handler for servicing unauthenticated user requests."""

    @webapp2.cached_property
    def current_user(self):
        return users.get_current_user()

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()


class BaseCronHandler(BaseHandler):
    """Base handler for servicing Cron requests.
    """

    def dispatch(self):
        """Ensure the "X-Appengine-Cron" header is set to "true"

        Ref: (https://cloud.google.com/appengine/docs/python/config/cron
        #securing_urls_for_cron)
        """
        header = self.request.headers.get('X-AppEngine-Cron', 'false')
        if header != 'true':
            raise SecurityError('X-AppEngine-Cron header missing')
        super(BaseCronHandler, self).dispatch()


class BaseTaskHandler(BaseHandler):
    """Base handler for task requests.
    """

    def dispatch(self):
        """Ensure a valid "X-Appengine-Cron" header is passed in the requests

        Ref: (https://cloud.google.com/appengine/docs/python/taskqueue/push/
        creating-handlers#securing_task_handler_urls)
        """
        header = self.request.headers.get('X-AppEngine-QueueName', None)
        if not header:
            raise SecurityError('X-AppEngine-QueueName header missing')
        super(BaseTaskHandler, self).dispatch()
