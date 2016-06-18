# Local imports
from modules.core.handlers import BaseHandler


class Frontend(BaseHandler):

    def get(self):
        self.render('home.html')
