# Local imports
from base.handlers.templates import BaseTemplateHandler
from base.handlers.templates import ModelListTemplatetHandler
from base.handlers.templates import ModelDetailTemplateHandler


class PageHandler(BaseTemplateHandler):
    pass


class AdminLisTemplatetHandler(ModelListTemplatetHandler):
    pass


class AdminDetailTemplateHandler(ModelDetailTemplateHandler):
    pass
