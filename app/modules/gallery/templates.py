# Local imports
from base.handlers import BaseHandler


class Frontend(BaseHandler):

    def get(self):
        self.render('gallery.html')
