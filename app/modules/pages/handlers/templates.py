# Local imports
from base.handlers.templates import BaseTemplateHandler
from modules.admin.handlers import AdminListTemplatetHandler
from modules.admin.handlers import AdminDetailTemplatetHandler
from modules.pages.modules import PageModules


class PageHandler(BaseTemplateHandler):
    pass


class ListTemplateHandler(AdminListTemplatetHandler):

    def get_queryset(self):
        """Fetch all the model records for the active locale
        """
        dataset = []
        for label, model in PageModules.page_models():
            record = model.get_published().to_dict()
            dataset.append({label: record})

        return dataset


class DetailTemplateHandler(AdminDetailTemplatetHandler):

    pass
