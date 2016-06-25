# Local imports
from base.handlers.templates import BaseTemplateHandler
from base.handlers.templates import ModelListTemplatetHandler
from base.handlers.templates import ModelDetailTemplateHandler
from modules.pages.models import PageNav


class PageHandler(BaseTemplateHandler):
    pass

class ListTemplateHandler(ModelListTemplatetHandler):

    model = PageNav
    template_name = '/admin/list.html'
    template_values = {
        'title': 'Pages',
        'description': 'Populate page content of the site'
    }


class DetailTemplateHandler(ModelDetailTemplateHandler):

    template_name = '/admin/form.html'
