# Local imports
from modules.pages.templates import BaseTemplateHandler


class PublicTemplateHandler(BaseTemplateHandler):

    def get(self):
        self.render('gallery.html')
