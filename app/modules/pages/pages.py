# Third-party imports
from webapp2 import Route

# Local imports
from base.modules import Module


def register_module():
    routes = [
        (
            r'/admin/pages',
            'modules.pages.handlers.templates.AdminListTemplateHandler'
        ),
        Route(
            '/admin/pages/<key:\w+>',
            'modules.pages.handlers.templates.AdminListTemplateHandler'
        ),
    ]

    return Module(
        name='pages',
        routes=routes
    )
