# stdlib imports
from datetime import datetime

# third-party imports
from wtforms import DateTimeField


class TimeField(DateTimeField):
    """Same as DateTimeField, except stores a `datetime.time`.
    """
    def __init__(self, label=None, validators=None, format='%H:%M:%S', **kwargs):
        super(TimeField, self).__init__(label, validators, format, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = datetime.strptime(date_str, self.format).time()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid time value'))
