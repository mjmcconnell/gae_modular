# third-party imports
from wtforms import Form
from wtforms import BooleanField
from wtforms import DateField
from wtforms import DateTimeField
from wtforms import DecimalField
from wtforms import FileField
from wtforms import FloatField
from wtforms import IntegerField
from wtforms import HiddenField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SelectMultipleField
from wtforms import TextAreaField
from wtforms import validators

# local imports
from base.utils.form_fields import TimeField
from base.utils import form_validators


# Match field types with a wtforms field, and optional validator
WTFORMS_FIELD_MAPPING = {
    'Boolean': BooleanField,
    'String': StringField,
    'Date': DateField,
    'DateTime': DateTimeField,
    'Decimal': DecimalField,
    'Email': (StringField, [validators.Email]),
    'File': FileField,
    'Float': FloatField,
    'Hidden': HiddenField,
    'ImageFile': FileField,
    'Integer': IntegerField,
    'Key': StringField,
    'Select': SelectField,
    'SelectMultiple': SelectMultipleField,
    'Text': TextAreaField,
    'Time': TimeField,
    'Url': (StringField, [form_validators.URL]),
}


class SerialiserField(object):

    validators = []

    def __init__(
            self, label, f_type, desc='', read_only=False, validators=None):
        self.desc = desc
        self.field_type = f_type
        self.label = label
        self.read_only = read_only

        if validators:
            self.validators = validators

    def __call__(self):
        default_validators = []
        _field = WTFORMS_FIELD_MAPPING.get(self.field_type)
        if isinstance(_field, tuple):
            _field = _field[0]
            default_validators = _field[1]

        validators = default_validators + self.validators

        field = _field(
            self.label,
            validators=validators,
            description=self.desc
        )

        return field, self.read_only


class Serialiser(object):

    pass

    # def __iter__(self):
    #     for field in self.fields.values():
    #         yield self[field.field_name]


class FormSerialiser(Serialiser):

    def populate_form(self):
        form = Form



class ModelSerialiser(FormSerialiser):

    ModelClass = None
    record = None

    def __init__(self):
        self.ModelClass = self.Meta.model
        self.field_names = self.Meta.field_names

    def _get_field(self, field_name):
        if hasattr(self, field_name):
            field = getattr(self, field_name)
        else:

            model_field = getattr(self.ModelClass, field_name)
            mode_type = model_field.__class__.__name__
            cleaned_model_type = mode_type.replace('Property', '')

            field = self.field_mapping.get(cleaned_model_type)

        validators = None
        visible = True



        return field, visible, validators

    def _get_field_names(self):
        """Returns a list of the fields for serialisation
        """
        if hasattr(self.Meta, 'fields'):
            return self.Meta.fields

        field_names = []
        for prop in self.ModelClass._properties.itervalues():
            field_names.append(prop._code_name)

        return field_names

    def _serialise_field(self, field_name):
        """Converts a ModelClass record instance to a serialisable dictionary
        """
        pass

    def serialise(self, depth=0):
        """Converts a ModelClass record instance to a serialisable dictionary

        Depth parameter used to fetch key properties nested inside the
        record instance
        """
        pass

    def get_fields(self):
        field_names = self._get_field_names()

    # Model iteractions

    def query(self, **kwargs):
        """Perform a datastore query agaisnt the ModelClass
        """
        return self.ModelClass.fetch_queried_records(kwargs)

    def get(self, key):
        """Gets a record from the datastore
        """
        self.record = self.ModelClass.get_by_key(key)
        return self.record

    def create(self, form_data):
        """Create a new record for the ModelClass
        """
        record = self.ModelClass.create(form_data)
        return self.serialise(record)

    def update(self, record, form_data):
        """Updates an existing record of the ModelClass
        """
        self.record.update(form_data)
        return self.serialise(self.record)
