# third-party imports
from wtforms import validators


class URL(validators.URL):
    """A validator overwites the wtforms URL validator to allow for relative urls.
    """

    other_field_name = None
    exta_validators = []

    def __init__(self, allow_relative=True, require_tld=True, message=None):
        super(URL, self).__init__(require_tld, message)
        self.allow_relative = allow_relative

    def __call__(self, form, field, message=None):
        # allow relatie urls
        if self.allow_relative and field.data.startswith('/'):
            return

        return super(URL, self).__call__(form, field, message)
