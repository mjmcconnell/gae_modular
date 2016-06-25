# future imports
from __future__ import absolute_import

# Local imports
from base.modules import Module
from modules.admin.modules import fetch_routes


def register_module():
    routes = fetch_routes()

    return Module(
        name='admin',
        routes=routes
    )
