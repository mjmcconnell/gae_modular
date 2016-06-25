# loacl imports
from base.modules import Module
from modules.admin.modules import AdminModule


def register_module():

    def on_load():
        AdminModule(
            name='pages',
            label='Pages',
            template_actions=['list', 'detail'],
            # api_actions=['read', 'update', 'delete']
        ).load()

    return Module(
        name='pages',
        on_load=on_load
    )
