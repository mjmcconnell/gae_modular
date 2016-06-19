# Local imports
from modules.pages.templates import PublicPageTemplateHandler
from modules.pages.templates import AdminPageListTemplatetHandler
from modules.pages.templates import AdminPageDetailTemplateHandler


class PublicTemplateHandler(PublicPageTemplateHandler):

    def get(self):
        self.render('gallery.html')


class AdminLisTemplatetHandler(AdminPageListTemplatetHandler):
    pass


class AdminDetailTemplateHandler(AdminPageDetailTemplateHandler):
    pass
