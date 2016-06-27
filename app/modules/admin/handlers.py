# future imports
from __future__ import absolute_import

# stdlib imports
import os

# local imports
from base.handlers.templates import BaseTemplateHandler
from base.handlers.templates import ModelListTemplatetHandler
from base.handlers.templates import ModelDetailTemplateHandler
from modules.admin.menus import Menu


TEMPLATE_DIR = os.path.normpath(os.path.dirname(__file__)) + '/templates'


class BaseAdminTemplateHandler(object):

    TEMPLATE_DIRS = [TEMPLATE_DIR]

    def render(self, template_name, template_values=None):
        """Renders the populated template to the response."""
        menu_groups = Menu.fetch_all()

        content = self.render_to_string(template_name, template_values)
        template = self.render_to_string(
            'admin.html',
            {
                'content': content,
                'description': template_values.get('description'),
                'menu_groups': menu_groups,
                'title': template_values.get('title'),
            }
        )
        self.response.out.write(template)


class AdminTemplatetHandler(
        BaseAdminTemplateHandler, BaseTemplateHandler):

    pass


class AdminListTemplatetHandler(
        BaseAdminTemplateHandler, ModelListTemplatetHandler):

    pass


class AdminDetailTemplatetHandler(
        BaseAdminTemplateHandler, ModelDetailTemplateHandler):

    pass
