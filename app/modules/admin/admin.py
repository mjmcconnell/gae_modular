# future imports
from __future__ import absolute_import

# third-party imports
from webapp2 import Route

# loacl imports
from base.modules import Module
from base.utils.routes import MultiPrefixRoute
from modules.admin.menus import MenuItem


def register_module():

    templates_routes = MultiPrefixRoute(
        handler_pfx='modules.admin.handlers.',
        name_pfx='admin-dashboard-template-',
        path_pfx='/admin',
        routes=[
            Route(r'', 'TemplateHandler', name='admin-dashboard'),
        ]
    ).routes

    def on_load():
        MenuItem(
            name='admin-dashboard',
            label='Dashboard',
            path='/admin',
        ).add()

    return Module(
        name='admin',
        on_load=on_load,
        routes=templates_routes
    )
