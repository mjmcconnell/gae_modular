from base.modules import Module
from modules.gallery.models import GalleryPage


def register_module():
    routes = [
        (r'/gallery', 'modules.gallery.handlers.templates.PublicTemplateHandler'),
    ]

    def on_load():
        """Register the page
        """
        GalleryPage.register()

    return Module(
        routes=routes,
        on_load=on_load
    )