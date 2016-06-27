# future imports
from __future__ import absolute_import

# local imports
from base.modules import Module
from modules.home.models import HomePage
from modules.pages.modules import PageModule


def register_module():
    routes = [
        (r'/', 'modules.home.handlers.templates.Frontend'),
    ]

    def on_load():
        """Register the page
        """
        PageModule(
            name='home',
            label='Home',
            model=HomePage
        ).load()

    return Module(
        name='home',
        routes=routes,
        on_load=on_load
    )
