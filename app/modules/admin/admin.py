# Local imports
from base.modules import Module
from modules.admin.registry import fetch_routes


def register_module():
    routes = fetch_routes()

    return Module(
        name='admin',
        routes=routes
    )
