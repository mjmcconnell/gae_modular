# Local imports
from base.handlers.templates import BaseTemplateHandler
from base.handlers.templates import ModelListTemplatetHandler
# from base.handlers.templates import ModelDetailTemplateHandler
from modules.pages.models import PageNav


class PageHandler(BaseTemplateHandler):
    pass


class LisTemplatetHandler(ModelListTemplatetHandler):

    model = PageNav
    template_name = '/list.html'
