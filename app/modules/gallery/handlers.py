# Local imports
from modules.pages.handlers.templates import PageHandler


class TemplateHandler(PageHandler):

    def get(self):
        self.render('gallery.html')