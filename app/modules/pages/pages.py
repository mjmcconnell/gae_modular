# future imports
from __future__ import absolute_import

# third-party imports
from webapp2 import Route

# loacl imports
from base.modules import Module
from base.utils.routes import MultiPrefixRoute
from modules.admin.menus import MenuItem


def register_module():

    api_routes = MultiPrefixRoute(
        handler_pfx='modules.pages.handlers.apis.',
        name_pfx='api-pages-',
        path_pfx='/api/pages',
        routes=[
            Route(r'', 'ListApiHandler', name='list'),
            Route(r'/<key:[a-z]>', 'ReadApiHandler', name='read'),
            Route(r'/<key:[a-z]>', 'UpdateApiHandler', name='update'),
        ]
    ).routes
    templates_routes = MultiPrefixRoute(
        handler_pfx='modules.pages.handlers.templates.',
        name_pfx='admin-pages-template-',
        path_pfx='/admin/pages',
        routes=[
            Route(r'', 'ListTemplateHandler', name='list'),
            Route(r'/<key:[a-z]>', 'DetailTemplateHandler', name='detail'),
        ]
    ).routes

    def on_load():
        MenuItem(
            name='pages',
            label='Pages',
            path='/admin/pages',
        ).add()

    return Module(
        name='pages',
        on_load=on_load,
        routes=api_routes + templates_routes
    )
