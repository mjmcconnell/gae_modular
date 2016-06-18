# Local imports
from base.handlers.base import BaseTemplateHandler


class Frontend(BaseTemplateHandler):

    def get(self):
        self.render('gallery.html')
