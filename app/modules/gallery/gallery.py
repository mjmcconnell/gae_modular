# local imports
from base.modules import Module
from modules.gallery.models import GalleryPage
from modules.pages.modules import PageModule


def register_module():
    routes = [
        (r'/gallery', 'modules.gallery.handlers.TemplateHandler'),
    ]

    def on_load():
        """Register the page
        """
        PageModule(
            name='gallery',
            label='Gallery',
            model=GalleryPage
        ).load()

    return Module(
        name='gallery',
        routes=routes,
        on_load=on_load
    )
