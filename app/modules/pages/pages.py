# third-party imports
from webapp2 import Route

# loacl imports
from base.modules import Module


def register_module():

    routes = [
        Route(
            r'/admin/pages',
            'modules.pages.handlers.templates.LisTemplatetHandler'
        ),
    ]

    return Module(
        name='pages',
        routes=routes
    )
