"""Generic admin template funtions used for rendering datastore records.
"""
# stdlib imports
import json

# local imports
from base.handlers.base import BaseTemplateHandler


class AdminListHandler(BaseTemplateHandler):
    """Generic list handler for Admin templates.

    Fetches all the records for the active model and renders the template.
    """

    template_values = None

    def get_queryset(self):
        """Fetch all the model records for the active locale
        """
        dataset = self.model.get_cached_dataset(self.parent_key)
        if self.child_model:
            for r in dataset:
                child_parent_key = self.child_model.build_parent_key(
                    self.locale_key.id(),
                    {self.model.__name__: r['id']}
                )
                r['children'] = self.child_model.get_cached_dataset(child_parent_key)

        return dataset

    def get(self, *args, **kwargs):
        records = self.get_queryset()
        if self.template_values is None:
            self.template_values = {}

        self.template_values.update({
            'json_records': json.dumps(records),
        })
        self.render('rest/list.html', self.template_values)


class AdminDetailHandler(BaseTemplateHandler):
    """Generic detail handler for Admin templates.

    Renders for form template, and if a key is found in the url, it will
    populate the json_record variable, to populate the form content
    """

    form = None

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
        self.render('rest/form.html', self.template_values)