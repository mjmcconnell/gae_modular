from base.modules import Module
from modules.home.models import HomePage


def register_module():
    routes = [
        (r'/', 'modules.home.handlers.templates.Frontend'),
    ]

    def on_load():
        """Register the page
        """
        HomePage.register()

    return Module(
        name='home',
        routes=routes,
        on_load=on_load
    )
