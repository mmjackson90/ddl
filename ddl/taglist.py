"""Adds a class to store and retrieve names of components, given their tags"""


class TagList:
    """
    A class that stores and retrieves names of components given their
    tag lists. Basically a fancy lookup class for faster/easier tag handling.
    """
    def __init__(self):
        self.tag_components = {}

    def add_component_to_tag(self, tag, component_name):
        self.tag_components.setdefault(tag, set()).add(component_name)

    def add_component(self, component):
        component_id = component.get_full_id()
        for tag in component.tags:
            self.add_component_to_tag(tag, component_id)

    def append(self, taglist):
        tag_components = taglist.tag_components
        for tag, components in tag_components.items():
            self.tag_components.setdefault(tag,
                                           set()).update(components)
