# Local imports
from modules.pages.handlers.templates import PageHandler


class Frontend(PageHandler):

    def get(self):
        self.render('gallery.html')
