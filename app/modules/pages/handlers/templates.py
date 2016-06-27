# stdlib imports
import json

# Local imports
from base.handlers.templates import BaseTemplateHandler
from modules.admin.handlers import AdminTemplatetHandler
# from modules.admin.handlers import AdminListTemplatetHandler
from modules.admin.handlers import AdminDetailTemplatetHandler
from modules.pages.modules import PageModules


class PageHandler(BaseTemplateHandler):
    pass


class ListTemplateHandler(AdminTemplatetHandler):

    template_name = '/admin/list.html'

    def get_queryset(self):
        """Fetch all the model records for the active locale
        """
        dataset = []
        for label, model in PageModules.page_models():
            record = model.get_published().to_dict()
            dataset.append({label: record})

        return dataset

    def get(self, *args, **kwargs):
        records = self.get_queryset()
        self.template_values = {}

        self.template_values.update({
            'json_records': json.dumps(records),
        })
        self.render(self.template_name, self.template_values)


class DetailTemplateHandler(AdminDetailTemplatetHandler):

    template_name = '/admin/form.html'
