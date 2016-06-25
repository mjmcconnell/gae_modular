"""Base template handlers for modules
"""
# future imports
from __future__ import absolute_import

# stdlib imports
import inspect
import jinja2
import json
import os
import webapp2

# local imports
from base import config
from base.handlers.common import BaseHandler


class BaseTemplateHandler(BaseHandler):

    TEMPLATE_DIRS = []

    @webapp2.cached_property
    def jinja2(self):
        template_dirs = [config.BASE_TEMPLATE_DIR] + self.TEMPLATE_DIRS
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


class ModelListTemplatetHandler(BaseTemplateHandler):
    """Generic list handler for Admin templates.

    Fetches all the records for the active model and renders the template.
    """

    child_model = None
    model = None
    template_name = None
    template_values = None

    def get_queryset(self):
        """Fetch all the model records for the active locale
        """
        dataset = self.model.fetch_cached_dataset()
        if self.child_model:
            for r in dataset:
                child_parent_key = self.child_model.build_parent_key(
                    self.locale_key.id(),
                    {self.model.__name__: r['id']}
                )
                r['children'] = self.child_model.fetch_cached_dataset(child_parent_key)

        return dataset

    def get(self, *args, **kwargs):
        records = self.get_queryset()
        if self.template_values is None:
            self.template_values = {}

        self.template_values.update({
            'json_records': json.dumps(records),
        })
        self.render(self.template_name, self.template_values)


class ModelDetailTemplateHandler(BaseTemplateHandler):
    """Generic detail handler for Admin templates.

    Renders for form template, and if a key is found in the url, it will
    populate the json_record variable, to populate the form content
    """

    form = None
    model = None
    template_values = None

    def _get_record(self):
        """Fetches a record using the key, passed into the url.
        """

        key = self.request.route_kwargs.get('key')
        if key:
            return self.model.get_by_urlsafe_key(key)
        return None

    def populate_form(self, record):
        """Populate the form."""

        return self.form(self.request.POST, record)

    def get(self, key=None, *args, **kwargs):
        """Handles the rendering and processing of a model form.
        """

        record = self._get_record()
        if key and record is None:
            self.abort(404)

        self.form = self.populate_form(record)

        if self.template_values is None:
            self.template_values = {}

        self.template_values.update({'form': self.form})

        if record:
            self.template_values.update({
                'json_record': json.dumps(record.to_dict()),
            })
        self.render('model/form.html', self.template_values)
