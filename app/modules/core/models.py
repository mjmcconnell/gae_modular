"""Core datastore models and base modals.
"""
# future imports
from __future__ import absolute_import

# stdlib imports
import datetime
import logging
import uuid
from collections import OrderedDict

# third-party imports
from google.appengine.api import memcache
from google.appengine.ext import ndb


def get_session_key():
    """Returns a random value, used for all sessions for the app
    """
    config_record = Config.get_record()
    return config_record.session_key


class Config(ndb.Model):
    """Modal for storing sensitive app data
    """

    session_key = ndb.BlobProperty()

    @classmethod
    def get_record(cls):
        record = cls.query().get()
        if record is None:
            record = Config()
            record.session_key = uuid.uuid4()
            record.put()
        return record


class BaseModel(ndb.Model):
    """Common data/operations for all storage models
    """

    cache_keys = []
    sort_order = None

    @classmethod
    def _post_delete_hook(cls, key, future):
        cls.clear_cache()

    def _post_put_hook(self, future):
        self.clear_cache()

    @classmethod
    def clear_cache(cls):
        queryset_key = cls.get_cache_key()
        memcache.delete(queryset_key)

        # Clean up any cached records
        if cls.cache_keys:
            memcache.delete_multi(cls.cache_keys)

    @classmethod
    def get_cache_key(cls, *args):
        _parts = [cls.__name__]
        for arg in args:
            _parts.append(str(arg))
        return '-'.join(_parts)

    @classmethod
    def get_queryset(cls):
        queryset = cls.query()
        if cls.sort_order:
            queryset = queryset.order(getattr(cls, cls.sort_order))
        return queryset

    @classmethod
    def fetch_cached_dataset(cls):
        """Fetches model related data from memcache,
        If no records are found then fetches them directly from the datastore,
        and adds the results into memcache for future references.

        Returns the matched records in dictionary format
        """
        # Build the cache key using the model name and locale id
        cache_key = cls.get_cache_key()

        dataset = memcache.get(cache_key)
        if dataset is None:
            dataset = []
            # Store the queried data in memcache for 1 day
            for r in cls.get_queryset().fetch():
                dataset.append(r.to_dict())
            memcache.add(cache_key, dataset, 86400)

        return dataset

    @classmethod
    def group_by(cls, group_property):
        """Groups a queryset by on of the properties of the modal
        """
        cache_key = cls.get_cache_key('group_by', group_property)

        grouped_records = memcache.get(cache_key)
        if not grouped_records:
            grouped_records = OrderedDict()
            for p in cls.fetch_cached_dataset():
                grouped_records.update({p[group_property]: p})

            # Store the queried data in memcache for 1 day
            memcache.add(cache_key, grouped_records, 86400)

        return grouped_records

    def to_dict(self, flatten=False):
        """Serialise model instance to a dictionary (to make it play nice with
        json.dumps())
        """
        d = super(BaseModel, self).to_dict()
        if flatten:
            flat_record = {}
            for k, v in self.serialise(d).iteritems():
                if type(v) is not dict:
                    flat_record[k] = v
                else:
                    label = '{}__'.format(k)
                    for ck, cv in v.iteritems():
                        flat_record[label + ck] = cv

            return flat_record

        return self.serialise(d)

    def serialise(self, _dict):
        serialised_dict = {}
        serialised_dict['id'] = self.key.id()
        serialised_dict['ukey'] = self.key.urlsafe()

        # Fetch any child records as well, as any ndb keys in the dict
        # will break json serialisation.
        for prop, value in _dict.iteritems():
            if type(value) == ndb.Key:
                try:
                    serialised_dict[prop] = value.get().to_dict()
                except Exception as e:
                    logging.error(e)
            elif isinstance(value, datetime.datetime):
                serialised_dict[prop] = str(value)
            elif isinstance(value, datetime.date):
                serialised_dict[prop] = str(value)
            elif isinstance(value, datetime.time):
                serialised_dict[prop] = str(value)
            else:
                serialised_dict[prop] = value

        return serialised_dict

    @classmethod
    def create(cls, form, defaults=None):
        """Create a new bdn record, from a submitted form.
        """
        record = cls()
        # Update the new record with default values
        if defaults:
            for key, value in defaults.iteritems():
                setattr(record, key, value)

        return record.update(form)

    def update(self, form):
        """Update a records property values from a form's request data.
        """
        child_records = {}
        for field in form:
            # The "__" is used to identify child properties
            if '__' in field.name:
                child_model, field_name = field.name.split('__')
                c_record = child_records.get(child_model)
                if c_record is None:
                    c_record = getattr(self, child_model).get()
                    child_records.update({child_model: c_record})
                setattr(c_record, field_name, field.data)

        # Save all the updated child records
        if child_records:
            for r in child_records:
                r.put()

        # Populate the record with the form request data
        form.populate_obj(self)
        # Save the record to the datastore
        return self.put().get()
