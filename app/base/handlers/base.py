"""Base handlers for modules
"""
# future imports
from __future__ import absolute_import

# stdlib imports
import jinja2
import inspect
import os
import webapp2

# third-party imports
from google.appengine.api import users
from webapp2_extras import sessions

# local imports
from base import config


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


class BaseTemplateHandler(BaseHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Directory of the "core" module, used for global templates
        base_dir = os.path.join(os.path.dirname(__file__))
        # Directory of the handler used for rendering the template,
        # for module specific templates
        current_dir = os.path.dirname(inspect.getfile(self.__class__))

        dirs = [base_dir, current_dir]
        template_dirs = [os.path.join(x, os.pardir, 'templates') for x in dirs]

        extensions = ['jinja2.ext.autoescape', 'jinja2.ext.with_']
        env = jinja2.Environment(
            autoescape=True,
            auto_reload=config.DEBUG,
            loader=jinja2.FileSystemLoader(template_dirs),
            extensions=extensions,
        )
        for k, v in self.app.config['jinja2']['filters'].items():
            env.filters[k] = v
        return env

    def render_to_string(self, template_name, template_values=None):
        """Populates the template, and returns the template as a string"""
        if not template_values:
            template_values = {}

        # add any functions/constants defined in config to the context
        for k, v in self.app.config['jinja2']['globals'].items():
            try:
                template_values[k]
            except KeyError:
                template_values[k] = v

        # add common request-specific items to the context
        template_values['request'] = self.request
        template_values['session'] = self.session

        # render and return template as string
        t = self.jinja2.get_template(template_name)
        return t.render(template_values)

    def render(self, template_name, template_values=None):
        """Renders the populated template to the response."""
        template = self.render_to_string(template_name, template_values)
        self.response.out.write(template)


class BaseApiHandler(BaseHandler):

    def render_json(self, data):
        pass


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
