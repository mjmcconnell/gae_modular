"""Generic admin api method used for altering records in the datastore.
"""
# stdlib imports
import json

# local imports
from modules.portal.app.handlers.base import AdminAjaxHandler


class BaseApiHandler(AdminAjaxHandler):

    form = None
    model = None

    def _get_record(self, key):
        """Fetches a record using the key, passed into the url.
        """
        return self.model.get_by_urlsafe_key(key)

    def render_json(self, **kwargs):
        """Returns a json response
        The response should followi the guidelines from:
        https://labs.omniti.com/labs/jsend
        """
        if 'status' not in kwargs:
            kwargs['status'] = 'success'
        if 'data' not in kwargs:
            kwargs['data'] = None

        self.response.write(json.dumps(kwargs))

    def submit_form(self, record=None):
        return_data = {}
        # Populates the form with the post data
        self.form = self._populate_form(record)

        # Sumbit the form to the modal for creating/updating a record
        saved, msg = self._save_form(record)

        if saved:
            return_data['status'] = 'success'
            return_data['data'] = record
        else:
            return_data['status'] = 'fail'
            return_data['message'] = msg
            return_data['data'] = self.form.errors
            self.response.set_status(400)

        return self.render_json(return_data)

    def _populate_form(self, record=None):
        """Populate the form."""
        return self.form(self.request.POST, record)

    def _save_form(self, record):
        """Save form data to the datastore.
        Handles form submission and file uploads.
        """
        msg = 'Record could not be saved to datastore, please try again.'
        if self.form.validate():
            if record:
                record.update(self.form)
            else:
                record = self.model.create(self.form)

            msg = '{0} {1}'.format(
                self.model.__name__,
                ('added', 'edited')[int(bool(self.request.method == 'PUT'))],
            )
            return True, None
        else:
            msg = ('There are errors on your form, please correct these, ',
                    'before trying to submit the form again.')

        return False, msg


class AdminApiListHandler(BaseApiHandler):

    def get(self, *args, **kwargs):
        """Save form data to the datastore
        """
        records = self.model.fetch_cached_dataset()
        return self.render_json({
            'status': 'success',
            'data': records,
        })

    def post(self, *args, **kwargs):
        """Save form data to the datastore
        """
        self.submit_form()


class AdminApiDetailHandler(BaseApiHandler):

    def get(self, key, *args, **kwargs):
        record = self._get_record(key)
        if record is None:
            self.response.set_status(404)
            return self.render_json({
                'status': 'fail',
                'message': 'Record could not be found.',
            })

        return self.render_json({
            'status': 'success',
            'data': record,
        })

    def post(self, key, *args, **kwargs):
        record = self._get_record(key)
        if record is None:
            self.response.set_status(404)
            return self.render_json({
                'status': 'fail',
                'message': 'Record could not be found.',
            })

        self._submit_form(record)

    def put(self, key, *args, **kwargs):
        self.post(key, args, kwargs)

    def patch(self, key, *args, **kwargs):
        self.post(key, args, kwargs)

    def delete(self, key, *args, **kwargs):
        """Update the records position field.
        """
        record = self._get_record(key)
        if record is None:
            self.response.set_status(404)
            return self.render_json({
                'status': 'fail',
                'message': 'Record could not be found.',
            })

        record.key.delete()
        return self.render_json()


class AdminApiPositionHandler(BaseApiHandler):
    """Updates the user defined position of each models record in the datastore

    Expects a list of objects with an "key" attribrute for each record
    """

    def post(self, *args, **kwargs):
        """Update the records position field.
        """
        post_data = self.request.POST
        for i, key in enumerate(json.loads((post_data['keys']))):
            record = self._get_record(key)
            setattr(record, 'order', i)
            record.put()
