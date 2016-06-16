"""Base handlers for modules
"""
# stdlib imports
import jinja2
import webapp2

# third-party imports
from google.appengine.api import users
from webapp2_extras import sessions

# local imports
from modules.core import config


class BaseHandler(webapp2.RequestHandler):
    """Base handler for servicing unauthenticated user requests."""

    def __init__(self, request, response):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

    @webapp2.cached_property
    def current_user(self):
        return users.get_current_user()

    def dispatch(self):
        try:
            super(BaseHandler, self).dispatch()
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    @webapp2.cached_property
    def jinja2(self):
        extensions = ['jinja2.ext.autoescape', 'jinja2.ext.with_']
        env = jinja2.Environment(
            autoescape=True,
            auto_reload=config.DEBUG,
            loader=jinja2.FileSystemLoader(constants.TEMPLATE_DIR),
            extensions=extensions,
        )
        for k, v in self.app.config['jinja2']['filters'].items():
            env.filters[k] = v
        return env

    def render_to_string(self, template_name, template_values=None):
        """Renders template_name with template_values and returns as a string."""
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
        """Renders template_name with template_values and writes to the response."""
        self.response.out.write(self.render_to_string(template_name, template_values))
