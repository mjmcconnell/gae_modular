# future imports
from __future__ import absolute_import

# stdlib imports
import collections


class MenuItem(object):
    """A class that holds module information."""

    def __init__(self, name, label, group=None, path=None, placement=1):
        self._name = name
        self.label = label
        self.group = group
        self.path = path
        self.placement = placement

        Menu.modules[self._name] = self

    def add(self):
        """Preform setup steps for module"""
        if self._name not in Menu.enabled:
            Menu.enabled.add(self._name)
            if self.group:
                Menu.items.add('.'.join(self.group, self._name))
            else:
                Menu.groups.add(self._name)


class Menu(object):
    """A registry that holds all custom modules."""

    modules = collections.OrderedDict()
    enabled = set()
    groups = set()
    items = set()

    @classmethod
    def fetch_all(cls):
        group_items = {}
        for item in cls.items:
            module = cls.modules.get(item)
            if group_items.get(item) is None:
                group_items[item] = []

            group_items[item.split('.')[0]].append({
                'label': module.label,
                'path': module.path,
                'placement': module.placement,
            })

        menu = []
        for g_name in cls.groups:
            module = cls.modules.get(g_name)
            children = []
            if group_items.get(g_name):
                children = group_items[g_name]

            children.sort(key=lambda item: (item['placement'], item['label']))

            nav_group = {
                'label': module.label,
                'path': module.path,
                'placement': module.placement,
                'children': children
            }

            menu.append(nav_group)

        menu.sort(key=lambda item: (item['placement'], item['label']))

        return menu
